import mydao
import collectData
import requests
import time
'''
CREATE TABLE IF NOT EXISTS `team_easy`.`summonerDTO` (
  `accountId` VARCHAR(100) NULL,
  `profileIconId` INT NULL,
  `revisionDate` BIGINT NULL,
  `name` VARCHAR(50) NOT NULL,
  `id` VARCHAR(100) NULL,
  `puuid` VARCHAR(100) NULL,
  `summonerLevel` BIGINT NULL,
  `apikey` VARCHAR(100) NULL,
  PRIMARY KEY (`name`))
ENGINE = InnoDB
'''
#데이터베이스 접근 mydao.MyDAO // api키 관리 collectData.CollectData
class SummonerDto(mydao.MyDAO,collectData.CollectData) :
    #leagueEntryDTO 테이블 생성
    def createSummonerDtoTable(self):
        self.connectDB()
        sql =   '''
                CREATE TABLE IF NOT EXISTS `team_easy`.`summonerDTO` (
                  `accountId` VARCHAR(100) NULL,
                  `profileIconId` INT NULL,
                  `revisionDate` BIGINT NULL,
                  `name` VARCHAR(50) NOT NULL,
                  `id` VARCHAR(100) NULL,
                  `puuid` VARCHAR(100) NULL,
                  `summonerLevel` BIGINT NULL,
                  `apikey` VARCHAR(100) NULL,
                  PRIMARY KEY (`name`))
                ENGINE = InnoDB
                '''
        self.cur.execute(sql)
        self.conn.commit()
        print('create summonerDto table.')
        self.closeDB()

    #데이터베이스에서 summonerDto들을 얻어온다 start_num은 시작할 인덱스, amount는 몇개 출력
    def getLeagueEntryDtos(self,start_num,amount):
        self.connectDB()
        sql = f'SELECT * FROM leagueEntryDto LIMIT {start_num}, {amount}'
        self.cur.execute(sql)
        rows =self.cur.fetchall()
        self.closeDB()
        return rows

    #소환사이름으로 소환사정보를 받아온다
    def getSummonerDtoFromApi(self,summonerName,ak):
        uri = f'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}?api_key={ak}'
        print(uri)
        response = requests.get(uri)
        status_code = response.status_code
        data = response.json()
        return status_code, data


    #summonerDto 테이블을 채운다. api에서 데이터를 받아 insert를 여러번 반복
    def insertSummonerDtos(self):
        # path='apikey.txt'
        # self.setApikeyFromFile(path)
        self.setApikeyFromFile()
        start_num =0
        amount=20
        while True :
            rows=self.getLeagueEntryDtos(start_num,amount)
            if len(rows) == 0 :
                break
            max_row = len(rows)
            row_index =0
            self.changeApikey()
            while row_index < max_row :
                row =rows[row_index]
                summonerName =row[2]
                status_code, data = self.getSummonerDtoFromApi(summonerName,self.api_key)
                if status_code == 200 : #데이터 받는데 성공
                    self.insertSummonerDto(data)
                elif status_code == 429 : #사용량 제한 걸림
                    self.changeApikey()
                    continue
                row_index+=1
            start_num += amount

    #하나의 summonerDto를 insert한다
    def insertSummonerDto(self,dto):
        self.connectDB()
        print('type : ', type(dto), ' data : ', dto)
        keys = list(dto.keys())
        keys.append('apikey')
        values = list(dto.values())
        values.append(self.api_key)
        for i, v in enumerate(values):
            values[i] = self.transformForDB(v)
        p_list = ['%s' for _ in range(len(values))]

        sql = 'REPLACE INTO summonerDto('
        sql += ','.join(keys)
        sql += ') VALUES('
        sql += ','.join(p_list)
        sql += ')'
        print(sql)
        self.cur.execute(sql,values)
        self.conn.commit()
        print(dto['name'], dto['accountId'])
        self.closeDB()

if __name__ == '__main__':
    summonerDto = SummonerDto()
    summonerDto.createSummonerDtoTable()
    start_time = time.time()
    summonerDto.insertSummonerDtos()
    end_time = time.time()
    print('총 수행 시간 : %.2f초'%(end_time-start_time))

