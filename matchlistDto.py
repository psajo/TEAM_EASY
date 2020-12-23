import requests
import pymysql
import time

#APIKEY파일에서 읽기
def setApikey() :
    global api_keys, api_key
    with open('C:/Users/psajo/Desktop/apikey.txt', 'r') as f:
        api_keys = f.read().split()
    print('api_key리스트 : ',api_keys)
    api_key = api_keys[api_index]

#APIKEY 바꾸기
def changeApikey(key="") :
    global api_index,api_key
    if key !="" : #입력값이 있으면
        api_key = key
    else : #입력값이 없으면
        max_index = len(api_keys)
        api_index = api_index+1
        if api_index > max_index-1 : #index넘어갔을때
            api_index=0
        api_key = api_keys[api_index]

#conn, cur 얻기
def setConnCur() :
    global conn, cur
    conn = pymysql.connect(host=HOST,port=PORT,user=USER,passwd=PASSWD,db=DB,charset=CHARSET)
    cur = conn.cursor()

#conn, cur 닫기
def closeConnCur() :
    conn.commit()
    cur.close()
    conn.close()

#matchlist 테이블 만들기
def createMatchlistTable() :
    # 데이터베이스 연결
    setConnCur()

    sql =   'CREATE TABLE IF NOT EXISTS matchlistDto ( \
                gameId BIGINT, \
                PRIMARY KEY(gameId)\
            )'
    cur.execute(sql)
    conn.commit()
    print('create matchlist table.')
    closeConnCur()
#createMatchlistTable end

#selectSummoner
def selectSummoner(start=0, amount=1000) :
    setConnCur()
    sql = f'SELECT * FROM summonerDto limit {start}, {amount}'
    cur.execute(sql)
    rows = cur.fetchall()
    closeConnCur()
    return rows
#selectSummoner end

#match테이블에 값 넣기
def insertMatchlist(result_dict):
    print('result_dict ',result_dict)
    gameId = result_dict['gameId']
    sql = 'INSERT INTO matchlistDto('
    sql+=   'gameId'
    sql+=   ') VALUES('
    sql+=   str(gameId)
    sql+= ')'
    print(sql)
    try:
        cur.execute(sql)
        print('INSERT gameId : ',result_dict['gameId'])
        conn.commit()
    except:
        print(gameId,'중복.')
#insertMatch end

#티어,단계로 소환사이름들 얻기
#https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/hide%20on%20bush?api_key=RGAPI-c5b1b806-3cf1-4ff6-8e36-5174cb88f9f7
#TIER_LIST = ['CHALLENGER','GRANDMASTER','MASTER','DIAMOND','PLATINUM','GOLD','SILVER','BRONZE','IRON']
def saveMatchlist(rows) : #rows는 summoner 데이터들이 들어온다
    global api_key
    setConnCur()
    s_time = time.time()
    for row in rows :
        encryptedAccountId = row[0]
        api_key = row[-1]
        uri = f'https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/{encryptedAccountId}?queue=420&api_key={api_key}'
        response = requests.get(uri)
        status_code = response.status_code
        print('status_code : ', status_code)
        if status_code == 200: #api 성공시
            matches = response.json()['matches']
            for match in matches :
                insertMatchlist(match)
        elif status_code==429 : #api타임아웃 걸렸을때
            print('time out. ', api_key)
            time.sleep(2)
        else :
            time.sleep(0.1)
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
    createMatchlistTable()
    start_index = 0
    amount = 1000
    while True :
        rows = selectSummoner(start_index,amount)
        c = len(rows)
        print('row 수 : ',c)
        if c != 0 :
            saveMatchlist(rows)
            start_index+=amount
        else :
            break

