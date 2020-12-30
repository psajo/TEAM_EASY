import mydao
import collectData
import requests
import time
'''
CREATE TABLE IF NOT EXISTS `team_easy`.`matchDto` (
  `gameId` BIGINT NOT NULL,
  `participantIdentities` JSON NULL,
  `queueId` INT NULL,
  `gameType` VARCHAR(20) NULL,
  `gameDuration` BIGINT NULL,
  `teams` JSON NULL,
  `platformId` VARCHAR(10) NULL,
  `gameCreation` BIGINT NULL,
  `seasonId` INT NULL,
  `gameVersion` VARCHAR(20) NULL,
  `mapId` INT NULL,
  `gameMode` VARCHAR(20) NULL,
  `participants` JSON NULL,
  PRIMARY KEY (`gameId`))
ENGINE = InnoDB
'''
#데이터베이스 접근 mydao.MyDAO // api키 관리 collectData.CollectData
class MatchDto(mydao.MyDAO,collectData.CollectData) :
    #MatchDto 테이블 생성
    def createMatchDtoTable(self):
        self.connectDB()
        sql =   '''
                CREATE TABLE IF NOT EXISTS `team_easy`.`matchDto` (
                  `gameId` BIGINT NOT NULL,
                  `participantIdentities` MEDIUMTEXT NULL,
                  `queueId` INT NULL,
                  `gameType` VARCHAR(20) NULL,
                  `gameDuration` BIGINT NULL,
                  `teams` MEDIUMTEXT NULL,
                  `platformId` VARCHAR(10) NULL,
                  `gameCreation` BIGINT NULL,
                  `seasonId` INT NULL,
                  `gameVersion` VARCHAR(20) NULL,
                  `mapId` INT NULL,
                  `gameMode` VARCHAR(20) NULL,
                  `participants` MEDIUMTEXT NULL,
                  PRIMARY KEY (`gameId`))
                ENGINE = InnoDB
                '''
        self.cur.execute(sql)
        self.conn.commit()
        print('create matchDto table.')
        self.closeDB()

    #데이터베이스에서 matchReferenceDto들을 얻어온다 start_num은 시작할 인덱스, amount는 몇개 출력
    def getMatchReferenceDtos(self,start_num,amount):
        self.connectDB()
        sql = f'SELECT * FROM matchReferenceDto LIMIT {start_num}, {amount}'
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        self.closeDB()
        return rows

    #gameId로 MatchDto를 받아온다
    def getMatchDtoFromApi(self,gameId):
        # path = 'apikey.txt'
        # self.setApikeyFromFile(path)
        self.setApikeyFromFile()
        uri = f'https://kr.api.riotgames.com/lol/match/v4/matches/{gameId}?api_key={self.api_key}'
        print(uri)
        response = requests.get(uri)
        status_code = response.status_code
        data = response.json()
        return status_code, data

    #matchReferenceDto 테이블을 채운다. api에서 받은 데이터를 insert를 반복하여 채움
    def insertMatchDtos(self):
        start_num =0
        amount=1000
        while True :
            rows=self.getMatchReferenceDtos(start_num,amount)
            if len(rows) == 0 :
                break
            max_row = len(rows)
            row_index =0
            while row_index < max_row :
                row =rows[row_index]
                gameId =row[0]
                status_code, data = self.getMatchDtoFromApi(gameId)
                if status_code == 200 : #데이터 받는데 성공
                    self.insertMatchDto(data)
                elif status_code == 429 : #사용량 제한 걸림
                    self.changeApikey()
                    continue
                row_index+=1
            start_num += amount

    #하나의 matchReferenceDto를 insert한다
    def insertMatchDto(self,dto):
        self.connectDB()
        print('type : ', type(dto), ' data : ', dto)
        keys = list(dto.keys())
        values = list(dto.values())
        for i, v in enumerate(values):
            values[i] = self.transformForDB(v)
        p_list = ['%s' for _ in range(len(values))]
        sql = 'REPLACE INTO matchDto('
        sql += ','.join(keys)
        sql += ') VALUES('
        sql += ','.join(p_list)
        sql += ')'
        print(sql)
        print(values)
        self.cur.execute(sql,values)
        self.conn.commit()
        print(dto['gameId'],dto['participantIdentities'][0]['player']['summonerName'] ,dto['participants'][0]['participantId'], dto['participants'][0]['championId'])
        self.closeDB()

if __name__ == '__main__':
    matchDto = MatchDto()
    matchDto.createMatchDtoTable()
    start_time = time.time()
    matchDto.insertMatchDtos()
    end_time = time.time()
    print('총 수행 시간 : %.2f'%(end_time-start_time))



