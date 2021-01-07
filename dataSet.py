import mydao
import pandas as pd

class DataSet(mydao.MyDAO) :
    #챔피언아이디, 이름을 반환한다
    def getChampions(self):
        self.connectDB()
        sql = 'SELECT `id`,`key`,`name`,`tags` FROM championDto'
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        self.closeDB()
        df = pd.DataFrame(rows, columns=['id','key','name','tag'])
        return df

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
        self.connectDB()
        sql = "SELECT champion1, champion2,champion3, champion4, champion5, champion6, champion7,champion8, champion9, champion10,win FROM championDataSet"
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        df =self.loadTeamTag(rows)
        self.closeDB()
        return df

    #teamTag수치를 반환
    def loadTeamTag(self,rows):
        df = pd.read_excel('tag_psj.xlsx', sheet_name='Sheet1')
        df.set_index('챔피언', inplace=True)
        print(df.head(5))
        teamAB_tag = pd.DataFrame(columns=['탱커' ,'지속딜','폭딜' ,'포킹','보조','이동기(궁극제외, 대쉬)','CC','그랩','원거리','근거리' ,'AP' ,'AD' ,'탱커','지속딜','폭딜' ,'포킹' ,'보조','이동기(궁극제외, 대쉬)','CC' ,'그랩' ,'원거리' ,'근거리','AP', 'AD' ,'win'])
        print(len(teamAB_tag.columns))
        for row in rows :
            teamA = df.loc[ [row[0],row[1],row[2],row[3],row[4]] , :]
            teamB = df.loc[ [row[5],row[6],row[7],row[8],row[9]] , :]
            teamA_tag =teamA.sum()
            teamB_tag =teamB.sum()
            temp =pd.concat([teamA_tag,teamB_tag])
            temp['win'] = row[-1]
            temp =pd.DataFrame(temp).transpose()
            teamAB_tag = teamAB_tag.append(temp,ignore_index=True)
        print(teamAB_tag.head(5))

        return teamAB_tag

    #전체 챔피언들의 클래스를 분류한 데이터프레임을 반환
    def getChampClassDataFrame(self):
        self.connectDB()
        sql = 'SELECT distinct `tags` FROM championDto'
        self.cur.execute(sql)
        rows_tag =self.cur.fetchall()
        col =['championId']
        for row in rows_tag:
            col.append(row[0])
        df=pd.DataFrame( columns=col)
        sql = "SELECT `key`, `tags` FROM championDto"
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        for row in rows:
            df =df.append({"championId":row[0], f'{row[1]}': 1}, ignore_index=True)
        df = df.fillna(0)
        df = df.astype('int')
        self.closeDB()
        return df

    #각 팀의 챔피언 5명의 세분화된 태그를 합쳐서 하나의 행으로 구성한 데이터셋 만들어 데이터프레임으로 반환한다
    def getTeamChampClass(self):
        df =self.getChampClassDataFrame()
        df = df.set_index('championId')
        col =[]
        col.extend(list(df.columns))
        col.extend(list(df.columns))
        col.append('win')
        ret_df = pd.DataFrame(columns=col)
        self.connectDB()
        sql = "SELECT champion1, champion2,champion3, champion4, champion5, champion6, champion7,champion8, champion9, champion10,win FROM championDataSet"
        self.cur.execute(sql)
        rows =self.cur.fetchall()
        for row in rows :
            champs =row[:-1]
            win = row[-1]
            teamA = df.loc[list(champs[:5]), :]
            teamB = df.loc[list(champs[5:]), :]
            teamA_class = teamA.sum()
            teamB_class = teamB.sum()
            teamAB_class = pd.concat([teamA_class,teamB_class])
            teamAB_class['win']= win
            temp = pd.DataFrame(teamAB_class).transpose()
            ret_df = ret_df.append(temp,ignore_index=True)
        self.closeDB()
        return ret_df


if __name__ == '__main__':
    dataSet =DataSet()
    df = dataSet.getTeamChampClass()
    pd.set_option('display.max_columns', 100)
    print(df)
