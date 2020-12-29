import mydao
import collectData
import requests
import time

'''
CREATE TABLE IF NOT EXISTS `team_easy`.`leagueEntryDTO` (
  `leagueId` VARCHAR(100) NULL,
  `summonerId` VARCHAR(100) NULL,
  `summonerName` VARCHAR(50) NOT NULL,
  `queueType` VARCHAR(50) NULL,
  `tier` VARCHAR(50) NULL,
  `rank` VARCHAR(5) NULL,
  `leaguePoints` INT NULL,
  `wins` INT NULL,
  `losses` INT NULL,
  `hotStreak` TINYINT NULL,
  `veteran` TINYINT NULL,
  `freshBlood` TINYINT NULL,
  `inactive` TINYINT NULL,
  `miniSeries` JSON NULL,
  PRIMARY KEY (`summonerName`))
ENGINE = InnoDB
'''
class LeagueEntryDto(mydao.MyDAO,collectData.CollectData) :
    #leagueEntryDTO 테이블 생성
    def createLeagueEntryDtoTable(self):
        self.connectDB()
        sql =   '''
                CREATE TABLE IF NOT EXISTS `team_easy`.`leagueEntryDTO` (
                  `leagueId` VARCHAR(100) NULL,
                  `summonerId` VARCHAR(100) NULL,
                  `summonerName` VARCHAR(50) NOT NULL,
                  `queueType` VARCHAR(50) NULL,
                  `tier` VARCHAR(50) NULL,
                  `rank` VARCHAR(5) NULL,
                  `leaguePoints` INT NULL,
                  `wins` INT NULL,
                  `losses` INT NULL,
                  `hotStreak` TINYINT NULL,
                  `veteran` TINYINT NULL,
                  `freshBlood` TINYINT NULL,
                  `inactive` TINYINT NULL,
                  `miniSeries` JSON NULL,
                  PRIMARY KEY (`summonerName`))
                ENGINE = InnoDB
                '''
        self.cur.execute(sql)
        self.conn.commit()
        print('create leagueEntryDTO table.')
        self.closeDB()

    #api에서 데이터를 받아 반환
    def getJsonFromApi(self,queue,tier,division,page):
        path='C:/Users/kccistc/Desktop/apikey.txt'
        self.setApikeyFromFile(path)
        uri = f'https://kr.api.riotgames.com/lol/league-exp/v4/entries/{queue}/{tier}/{division}?page={page}&api_key={self.api_key}'
        print(uri)
        response = requests.get(uri)
        status_code = response.status_code
        data = response.json()
        return status_code,data

    #api를 이용하여 받은 데이터들을 insert 반복
    def insertLeagueEntriesByApi(self):
        queue = 'RANKED_SOLO_5x5'
        try :
            for tier in self.TIER_LIST:
                for division in self.DIVISION_LIST:
                    page = 1
                    while True:
                        status_code, data_list = self.getJsonFromApi(queue, tier, division, page)
                        print('status code ',status_code)
                        if status_code == 200:  # 데이터 받는데 성공
                            if data_list : #데이터가 있으면
                                for data in data_list :
                                    self.insertLeagueEntryDto(data)
                            else : # 데이터가 없을 때
                                break
                        elif status_code == 429:  # 이용제한 걸림
                            self.changeApikey()
                            continue
                        elif status_code == 403:  # apikey 만료
                            answer =input('apikey만료! 갱신한 다음 계속하기 Y, 그만하기 N')
                            if answer =='Y':
                                path='C:/Users/kccistc/Desktop/apikey.txt'
                                self.setApikeyFromFile(path)
                                continue
                            elif answer =='N' :
                                print('만료.')
                                assert False, str(status_code) + ', apikey 만료로 종료됨.'
                            else :
                                continue
                        elif status_code ==400 : #bad request 없는 페이지 요청했을때
                            break
                        else:
                            time.sleep(0.1)
                        page += 1
                        # 샘플로 1페이지씩만 받는다 여기부터
                        if page >= 2:
                            break
                        # 나중에 여기까지 지울 것
        except Exception as e: #apikey가 만료 되었을때 그만하기를 눌렀을 경우 여기로 온다
            print("예외 발생. ",e)

    #leagueEntryDto insert
    def insertLeagueEntryDto(self,data):
        self.connectDB()
        print('type : ', type(data),' data : ', data)
        keys = list(data.keys())
        values = list(data.values())
        for i ,v in enumerate(values) :
            values[i] =self.transformForDB(v)
        p_list = ['%s' for _ in range(len(values))]

        sql = 'REPLACE INTO leagueEntryDto('
        sql += ','.join(keys)
        sql += ') VALUES('
        sql += ','.join(p_list)
        sql += ')'
        print(sql)
        self.cur.execute(sql, values)
        print('INSERT ', data['summonerName'])
        self.conn.commit()
        self.closeDB()



if __name__ == '__main__':
    leagueEntry = LeagueEntryDto()
    leagueEntry.createLeagueEntryDtoTable()
    start_time = time.time()
    leagueEntry.insertLeagueEntriesByApi()
    end_time = time.time()
    print('수행 시간 : %.2f초'%(end_time-start_time))
