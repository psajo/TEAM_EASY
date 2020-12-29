import requests
import mydao

'''
CREATE TABLE IF NOT EXISTS `mydb`.`championDTO` (
  `version` VARCHAR(20) NOT NULL,
  `id` VARCHAR(20) NULL,
  `key` INT NOT NULL,
  `name` VARCHAR(50) NULL,
  `title` VARCHAR(50) NULL,
  `blurb` VARCHAR(1000) NULL,
  `info` JSON NULL,
  `image` JSON NULL,
  `tags` VARCHAR(100) NULL,
  `partype` VARCHAR(20) NULL,
  `stats` JSON NULL,
  PRIMARY KEY (`key`, `version`))
ENGINE = InnoDB
'''
class DataDragon(mydao.MyDAO) :
    #테이블 생성
    def createTable(self):
        self.connectDB()
        sql =   '''
                CREATE TABLE IF NOT EXISTS `championDTO` (
                  `version` VARCHAR(20) NOT NULL,
                  `id` VARCHAR(20) NULL,
                  `key` INT NOT NULL,
                  `name` VARCHAR(50) NULL,
                  `title` VARCHAR(50) NULL,
                  `blurb` VARCHAR(1000) NULL,
                  `info` JSON NULL,
                  `image` JSON NULL,
                  `tags` VARCHAR(100) NULL,
                  `partype` VARCHAR(20) NULL,
                  `stats` JSON NULL,
                  PRIMARY KEY (`key`, `version`))
                ENGINE = InnoDB
                '''
        self.cur.execute(sql)
        print('create championDTO table.')
        self.closeDB()

    #API URI에서 챔피언에 대한 정보를 받아 반환한다
    def getJsonFromUri(self,uri='http://ddragon.leagueoflegends.com/cdn/10.25.1/data/ko_KR/champion.json'):
        response = requests.get(uri)
        data = response.json()['data']
        return data

    #json데이터를 테이블에 저장한다
    def insertChampionDtos(self,jdata):
        self.connectDB()
        for champ in jdata:
            keys = jdata[champ].keys()
            keys = [f'`{k}`' for k in keys]  # 예약어랑 겹칠 수도 있기 때문에 문자열로 만들어준다
            # '"는 문자열 , `는 테이블명 컬럼명 longtext는 문자열로 감싸주어야 값이 들어감
            values = list(jdata[champ].values())
            p_list = ['%s' for _ in range(len(values))]
            for i, e in enumerate(values):
                values[i] = self.transformForDB(e)
            print('testing : ', values)
            sql = 'INSERT INTO championDTO('
            sql += ','.join(keys)
            sql += ') VALUES('
            sql += ','.join(p_list)
            sql += ')'
            print('sql : ',sql)
            print('값 : ', values)
            self.cur.execute(sql, values)
            self.conn.commit()
        self.closeDB()

    #데이터가 몇개 있는지 출력
    def printCount(self) :
        self.connectDB()
        sql = 'SELECT COUNT(*) FROM championDto'
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        print('champion table.')
        print(rows)
        self.closeDB()

if __name__ == '__main__':
    dd=DataDragon()
    dd.createTable()
    dd.printCount()
    try :
        dd.insertChampionDtos(dd.getJsonFromUri())
    except Exception as e:
        print(e)
    dd.printCount()