import mydao
import collectData
import requests
import time
'''
CREATE TABLE IF NOT EXISTS `team_easy`.`matchReferenceDto` (
  `gameId` BIGINT NOT NULL,
  `role` VARCHAR(20) NULL,
  `season` INT NULL,
  `platformId` VARCHAR(10) NULL,
  `champion` INT NULL,
  `queue` INT NULL,
  `lane` VARCHAR(10) NULL,
  `timestamp` BIGINT NULL,
  PRIMARY KEY (`gameId`))
ENGINE = InnoDB
'''
#데이터베이스 접근 mydao.MyDAO // api키 관리 collectData.CollectData
class MatchReferenceDto(mydao.MyDAO,collectData.CollectData) :
    #MatchReferenceDto 테이블 생성
    def createMatchReferenceDtoTable(self):
        self.connectDB()
        sql =   '''
                CREATE TABLE IF NOT EXISTS `team_easy`.`matchReferenceDto` (
                  `gameId` BIGINT NOT NULL,
                  `role` VARCHAR(20) NULL,
                  `season` INT NULL,
                  `platformId` VARCHAR(10) NULL,
                  `champion` INT NULL,
                  `queue` INT NULL,
                  `lane` VARCHAR(10) NULL,
                  `timestamp` BIGINT NULL,
                  PRIMARY KEY (`gameId`))
                ENGINE = InnoDB
                '''
        self.cur.execute(sql)
        self.conn.commit()
        print('create matchReferenceDto table.')
        self.closeDB()

    #데이터베이스에서 summonerDto들을 얻어온다 start_num은 시작할 인덱스, amount는 몇개 출력
    def getSummonerDtos(self,start_num,amount):
        self.connectDB()
        sql = f'SELECT * FROM summonerDto LIMIT {start_num}, {amount}'
        self.cur.execute(sql)
        rows =self.cur.fetchall()
        self.closeDB()
        return rows

    #encryptedAccountId로 MatchReference List를 받아온다
    def getMatchReferenceDtoFromApi(self,encryptedAccountId,ak):
        #'https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/5lrH1NlrseTtrRsuVMX2Jwy0pNY1s2TkoqrXTFQLqt3N?queue=420&beginTime=1601510400000&api_key=RGAPI-48feb493-cd51-4ce0-96f5-5be724f52a8d'
        uri = f'https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/{encryptedAccountId}?queue=420&beginTime=1601510400000&api_key={ak}'
        print(uri)
        response = requests.get(uri)
        status_code = response.status_code
        data = response.json()
        return status_code, data

    #matchReferenceDto 테이블을 채운다. api에서 받은 데이터를 insert를 반복하여 채움
    def insertMatchReferenceDtos(self):
        start_num =0
        amount=1000
        while True :
            rows=self.getSummonerDtos(start_num,amount)
            if len(rows) == 0 :
                break
            max_row = len(rows)
            row_index =0
            while row_index < max_row :
                row =rows[row_index]
                encryptedAccountId =row[0]
                ak = row[-1] #맨 마지막 인덱스가 apikey
                print(row[3],', ',row[0],', ',ak)
                status_code, data = self.getMatchReferenceDtoFromApi(encryptedAccountId,ak)
                if status_code == 200 : #데이터 받는데 성공
                    matches = data['matches']
                    for m in matches :
                        self.insertMatchReferenceDto(m)
                elif status_code == 429 : #사용량 제한 걸림
                    print('sleep... 10 sec.')
                    time.sleep(10)
                    continue
                row_index+=1
            start_num += amount


    #하나의 matchReferenceDto를 insert한다
    def insertMatchReferenceDto(self,dto):
        self.connectDB()
        print('type : ', type(dto), ' data : ', dto)
        keys = list(dto.keys())
        values = list(dto.values())
        for i, v in enumerate(values):
            values[i] = self.transformForDB(v)
        p_list = ['%s' for _ in range(len(values))]

        sql = 'REPLACE INTO matchReferenceDto('
        sql += ','.join(keys)
        sql += ') VALUES('
        sql += ','.join(p_list)
        sql += ')'
        print(sql)
        self.cur.execute(sql,values)
        self.conn.commit()
        print(dto['gameId'], dto['champion'])
        self.closeDB()

if __name__ == '__main__':
    matchReferenceDto = MatchReferenceDto()
    matchReferenceDto.createMatchReferenceDtoTable()
    start_time = time.time()
    matchReferenceDto.insertMatchReferenceDtos()
    end_time = time.time()
    print('총 수행 시간 : %.2f초'%(end_time-start_time))



