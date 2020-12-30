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
        print('api_index',api_index)
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

#데이터베이스에 participant테이블 만들기
def createParticipantTable() :
    # 데이터베이스 연결
    setConnCur()
    sql =   'CREATE TABLE IF NOT EXISTS participantDto('
    sql+=       'gameId BIGINT, '
    sql+=       'participantId INT, '
    sql +=      'championId INT,'
    sql +=      'winlose BOOLEAN,'
    sql +=      'PRIMARY KEY(gameId, participantId)'
    sql +=  ')'
    print(sql)
    cur.execute(sql)
    conn.commit()
    print('create participant table.')
    closeConnCur()
#createParticipantTable end ####

#selectMatchlist
def selectMatch(start=0, amount=1000) :
    setConnCur()
    sql = f'SELECT gameId, participants FROM matchDto WHERE gameVersion LIKE "10.%%" LIMIT {start}, {amount}'
    cur.execute(sql)
    rows = cur.fetchall()
    closeConnCur()
    return rows
#selectSummoner end

#match테이블에 값 넣기
def insertParticipant(gameId,result_dict):
    print('result_dict ',result_dict)
    keys =['gameId','participantId','championId','winlose']
    values=[gameId]
    values.append(result_dict['participantId'])
    values.append(result_dict['championId'])
    wl = result_dict['stats']['win']
    values.append(wl)
    p_list = [ '%s' for _ in range(len(values))]
    print(values)
    sql = 'REPLACE INTO participantDto('
    sql+=   ','.join(keys)
    sql+=   ') VALUES('
    sql+=   ','.join(p_list)
    sql+= ')'
    print(sql)
    cur.execute(sql,values)
    print('INSERT ',gameId,result_dict['championId'])
    conn.commit()
#insertMatch end

#티어,단계로 소환사이름들 얻기
#https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/hide%20on%20bush?api_key=RGAPI-c5b1b806-3cf1-4ff6-8e36-5174cb88f9f7
#TIER_LIST = ['CHALLENGER','GRANDMASTER','MASTER','DIAMOND','PLATINUM','GOLD','SILVER','BRONZE','IRON']
def saveMatch(rows) : #rows는 summoner 데이터들이 들어온다
    import ast
    setConnCur()
    count = 0

    for row in rows :
        gameId =row[0]
        row = ast.literal_eval(row[1])
        for p in row :
            insertParticipant(gameId,p)

    closeConnCur()

#saveMatch end


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
    createParticipantTable()
    start_index = 0
    amount = 10000
    s_time =time.time()
    while True :
        rows = selectMatch(start_index,amount)
        c = len(rows)
        print('row 수 : ',c)
        if c != 0 :
            saveMatch(rows)
            start_index+=amount
        else :
            break;
    print('경과시간 %.2f초'%(time.time() -s_time))
