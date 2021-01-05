import mydao
import pandas as pd

class DataSet(mydao.MyDAO) :
    #챔피언아이디와 승패여부가 저장될 championDataSet 테이블을 만든다.
    def createChampionDataSetTable(self):
        self.connectDB()
        sql = '''CREATE TABLE IF NOT EXISTS `team_easy`.`championDataSet` (
                  `gameId` BIGINT NOT NULL,
                  `champion1` INT NOT NULL,
                  `champion2` INT NOT NULL,
                  `champion3` INT NOT NULL,
                  `champion4` INT NOT NULL,
                  `champion5` INT NOT NULL,
                  `champion6` INT NOT NULL,
                  `champion7` INT NOT NULL,
                  `champion8` INT NOT NULL,
                  `champion9` INT NOT NULL,
                  `champion10` INT NOT NULL,
                  `win` TINYINT NOT NULL,
                  PRIMARY KEY (`gameId`))
                ENGINE = InnoDB'''
        self.cur.execute(sql)
        self.conn.commit()
        print('create championDataSet table.')
        self.closeDB()

    #match테이블에서 챔피언아이디와 승패여부만 추출하여 championDataSet테이블에 저장한다.
    def makeChampionsDataSet(self):
        self.connectDB()
        sql = "SELECT gameId FROM participantdto"
        self.cur.execute(sql)
        gameIds = self.cur.fetchall()
        for gameId in gameIds :
            sql = f"SELECT win FROM teamStatsDto WHERE gameId= '{gameId[0]}' AND teamId ='100'"
            self.cur.execute(sql)
            wins =self.cur.fetchall()
            if wins[0][0] == 'Win' :
                win = 1
            else :
                win =0
            sql = f"SELECT gameId, participantId, championId FROM participantdto WHERE gameId = '{gameId[0]}'"
            self.cur.execute(sql)
            rows = self.cur.fetchall()
            sql = 'INSERT INTO championDataSet(gameId, champion1, champion2,champion3, champion4, champion5, champion6, champion7,'
            sql += 'champion8, champion9, champion10,win) '
            sql += f'VALUES({rows[0][0]},{rows[0][2]},{rows[1][2]},{rows[2][2]},{rows[3][2]},{rows[4][2]},{rows[5][2]},{rows[6][2]},{rows[7][2]},{rows[8][2]},{rows[9][2]},{win})'
            print(sql)
            try :
                self.cur.execute(sql)
                self.conn.commit()
            except Exception as e :
                print(e)
        self.closeDB()

    #championDataSet에서 데이터를 받아 데이터프레임으로 반환한다
    def getChampionsDataSet(self):
        self.connectDB()
        sql ="SELECT champion1, champion2,champion3, champion4, champion5, champion6, champion7,champion8, champion9, champion10,win FROM championDataSet"
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        self.closeDB()
        columns = ['champion1', 'champion2','champion3', 'champion4', 'champion5', 'champion6', 'champion7','champion8', 'champion9', 'champion10','win']
        df = pd.DataFrame(rows, columns=columns)
        return df

    #각 팀의 챔피언 5명의 아이디를 받아 챔피언 태그로 변환한 데이터프레임을 반환한다
    def getChampTagDataSet(self):
        pass

    #각 팀의 챔피언 5명의 세분화된 태그를 합쳐서 하나의 행으로 구성한 데이터셋 만들어 데이터프레임으로 반환한다
    def getDetailTagDataSet(self):
        pass

if __name__ == '__main__':
    dataSet =DataSet()
    dataSet.createChampionDataSetTable()
    dataSet.makeChampionsDataSet()
    # df = dataSet.getChampionsDataSet()
    # print(df.head(5))
