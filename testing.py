import mydao
import collectData
import numpy as np
class Test(mydao.MyDAO, collectData.CollectData) :
    def extractJson(self,gameId) :
        self.connectDB()
        #gameId = 3479309056
        sql = f'SELECT teams,participants FROM matchDto WHERE gameId ={gameId}'
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        self.closeDB()
        return rows

if __name__ == '__main__':
    test = Test()
    gameId = 3479309056
    match1 = test.extractJson(gameId)
    print(match1[0][0])
    print(match1[0][1])
    print(type(match1[0][0]))

    import ast
    teams = ast.literal_eval(match1[0][0])
    print(type(teams[0]), teams[0]['win'])
    participant = ast.literal_eval(match1[0][1])
    print(type(participant[0]),participant[0]['championId'])
    row_list = [gameId,
                participant[0]['championId'],
                participant[1]['championId'],
                participant[3]['championId'],
                participant[4]['championId'],
                participant[5]['championId'],
                participant[6]['championId'],
                participant[7]['championId'],
                participant[8]['championId'],
                participant[9]['championId'],
                1 if teams[0]['win'] =='Win' else 0]
    print(row_list)
