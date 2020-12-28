import requests
import pymysql
import time

class CollectData :
    api_key = "";
    api_index = 0
    api_keys = []
    TIER_LIST = ['CHALLENGER', 'GRANDMASTER', 'MASTER', 'DIAMOND', 'PLATINUM', 'GOLD', 'SILVER', 'BRONZE',
                 'IRON']  # 티어이름 내림차순
    DIVISION_LIST = ['I', 'II', 'III', 'IV']
    HOST = 'localhost';
    PORT = 3306;
    USER = 'root';
    PASSWD = '1234';
    DB = 'teameasy';
    CHARSET = 'utf8'
    conn = None
    cur = None
    # APIKEY파일에서 읽기
    def setApikey(self):
        with open('C:/Users/psajo/Desktop/apikey.txt', 'r') as f:
            self.api_keys = f.read().split()
        print('api_key리스트 : ', self.api_keys)
        self.api_key = self.api_keys[self.api_index]
    # APIKEY 바꾸기
    def changeApikey(self,key=""):
        if key != "":  # 입력값이 있으면
            self.api_key = key
        else:  # 입력값이 없으면
            max_index = len(api_keys)
            self.api_index = self.api_index + 1
            if self.api_index > max_index - 1:  # index넘어갔을때
                self.api_index = 0
            print('api_index', self.api_index)
            self.api_key = self.api_keys[self.api_index]
    #conn, cur 얻기
    def setConnCur(self) :
        self.conn = pymysql.connect(host=self.HOST,port=self.PORT,user=self.USER,passwd=self.PASSWD,db=self.DB,charset=self.CHARSET)
        self.cur = self.conn.cursor()
    #conn, cur 닫기
    def closeConnCur(self) :
        conn.commit()
        cur.close()
        conn.close()

#데이터베이스에 match테이블 만들기
def createMatchTable() :
    # 데이터베이스 연결
    setConnCur()
    sql =   'CREATE TABLE IF NOT EXISTS matchDto('
    sql+=       'gameId BIGINT, '
    sql+=       'participantIdentities TEXT(10000), '
    sql +=      'queueId INT,'
    sql +=      'gameType VARCHAR(20),'
    sql +=      'gameDuration BIGINT,'
    sql +=      'teams TEXT(3000),'
    sql +=      'platformId VARCHAR(10),'
    sql +=      'gameCreation BIGINT,'
    sql +=      'seasonId INT,'
    sql +=      'gameVersion VARCHAR(20),'
    sql +=      'mapId INT,'
    sql +=      'gameMode VARCHAR(20),'
    sql +=      'participants TEXT(60000),'
    sql +=      'PRIMARY KEY(gameId)'
    sql +=  ')'
    print(sql)
    cur.execute(sql)
    conn.commit()
    print('create match table.')
    closeConnCur()
#createMatchTable end

#selectMatchlist
def selectMatchlist(start=0, amount=1000) :
    setConnCur()
    sql = f'SELECT * FROM matchlistDto limit {start}, {amount}'
    cur.execute(sql)
    rows = cur.fetchall()
    closeConnCur()
    return rows
#selectSummoner end

#match테이블에 값 넣기
def insertMatch(result_dict):
    print('result_dict ',result_dict)
    keys = result_dict.keys()
    values = list(result_dict.values())
    p_list = ['%s' for _ in range(len(values))]
    for i,v in enumerate(values) :
        if type(v) == bool :
            values[i] = int(v)
        if type(v) == dict:
            values[i] = str(v)
        if type(v) == list:
            values[i] = str(v)
    sql = 'REPLACE INTO matchDto('
    sql+=   ','.join(keys)
    sql+=   ') VALUES('
    sql+=   ','.join(p_list)
    sql+= ')'
    print(sql)
    print(values)
    cur.execute(sql,values)
    print('INSERT ',result_dict['gameId'])
    conn.commit()
#insertMatch end

#티어,단계로 소환사이름들 얻기
#https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/hide%20on%20bush?api_key=RGAPI-c5b1b806-3cf1-4ff6-8e36-5174cb88f9f7
#TIER_LIST = ['CHALLENGER','GRANDMASTER','MASTER','DIAMOND','PLATINUM','GOLD','SILVER','BRONZE','IRON']
def saveMatch(rows) : #rows는 summoner 데이터들이 들어온다
    setConnCur()
    s_time = time.time()
    count = 0
    while count<len(rows)-1:
        gameId = rows[count][0]
        # https://kr.api.riotgames.com/lol/match/v4/matches/4836191807?api_key=RGAPI-432cdf36-0e8c-418d-87d6-7d442b2de823
        uri = f'https://kr.api.riotgames.com/lol/match/v4/matches/{gameId}?api_key={api_key}'
        response = requests.get(uri)
        status_code = response.status_code
        print('status_code : ', status_code)
        if status_code == 200: #api 성공시
            match = response.json()
            insertMatch(match)
            count+=1
            continue
        elif status_code==429 : #api타임아웃 걸렸을때
            changeApikey()
            print('change API KEY. ', api_key)
            time.sleep(0.1)
            continue
        else :
            time.sleep(0.1)
        count+=1
    print('총 작업시간 : %0.4f초'%(time.time()-s_time))
    closeConnCur()

#getLeagueEntries end


#전역변수들
# API_KEY = 'RGAPI-432cdf36-0e8c-418d-87d6-7d442b2de823' #주기적으로 갱신 해줘야됨
api_key=""; api_index =0
api_keys =[]
TIER_LIST = ['CHALLENGER','GRANDMASTER','MASTER','DIAMOND','PLATINUM','GOLD','SILVER','BRONZE','IRON'] #티어이름 내림차순
DIVISION_LIST = ['I','II','III','IV']
HOST='20.194.19.37'; PORT=3306; USER='te'; PASSWD='1234'; DB='teameasy'; CHARSET='utf8'
conn = None
cur = None

if __name__ == '__main__':
    setApikey()
    createMatchTable()
    rows = selectMatchlist()
    print('row 수 : ',len(rows))
    saveMatch(rows)
