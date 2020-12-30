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

#데이터베이스에 player테이블 만들기
def createPlayerTable() :
    # 데이터베이스 연결
    setConnCur()
    sql =   'CREATE TABLE IF NOT EXISTS playerDto('
    sql+=       'gameId BIGINT, '
    sql+=       'participantId INT, '
    sql+=       'profileIcon INT, '
    sql+=       'accountId VARCHAR(100), '
    sql+=       'matchHistoryUri VARCHAR(100), '
    sql+=       'currentAccountId VARCHAR(100), '
    sql+=       'currentPlatformId VARCHAR(10), '
    sql+=       'summonerName VARCHAR(100), '
    sql+=       'summonerId VARCHAR(100), '
    sql+=       'platformId VARCHAR(10), '
    sql+=       'PRIMARY KEY(gameId, participantId)'
    sql +=  ')'
    print(sql)
    cur.execute(sql)
    conn.commit()
    print('create playerDto table.')
    closeConnCur()
#createPlayerTable end

#selectMatchlist
def selectParticipantIdentities(start=0, amount=1000) :
    setConnCur()
    sql = f'SELECT gameId,participantIdentities FROM matchDto limit {start}, {amount}'
    cur.execute(sql)
    rows = cur.fetchall()
    closeConnCur()
    return rows
#selectSummoner end

#match테이블에 값 넣기
def insertPlayerDto(gameId, result_dict):
    print('gameId : ',gameId,'result_dict ',result_dict)
    #,'profileIcon','accountId','matchHistoryUri','currentAccountId','currentPlatformId','summonerName','summonerId','platformId'
    keys = ['gameId' ,'participantId']
    values = list(result_dict.values())
    player_values = []
    player_values.append(gameId)
    player_values.append(values[0])
    p_keys =values[1].keys()
    keys.extend(list(p_keys))
    player_values.extend(list(values[1].values()))
    print('test',len(keys),keys)
    print('testv',len(player_values),player_values)
    p_list = ['%s' for _ in range(len(player_values))]
    for i,v in enumerate(values) :
        if type(v) == bool :
            values[i] = int(v)
        if type(v) == dict:
            values[i] = str(v)
        if type(v) == list:
            values[i] = str(v)
    sql = 'REPLACE INTO playerDto('
    sql+=   ','.join(keys)
    sql+=   ') VALUES('
    sql+=   ','.join(p_list)
    sql+= ')'
    print(sql)
    print(player_values)
    cur.execute(sql,player_values)
    print('INSERT playerDto ',gameId)
    conn.commit()
#insertMatch end

#티어,단계로 소환사이름들 얻기
#https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/hide%20on%20bush?api_key=RGAPI-c5b1b806-3cf1-4ff6-8e36-5174cb88f9f7
#TIER_LIST = ['CHALLENGER','GRANDMASTER','MASTER','DIAMOND','PLATINUM','GOLD','SILVER','BRONZE','IRON']
def savePlayers(rows) : #rows는 summoner 데이터들이 들어온다
    import ast
    setConnCur()
    for row_tuple in rows :
        gameId = row_tuple[0]
        row_participants =ast.literal_eval(row_tuple[1])
        for participant in row_participants:
            print(gameId,participant)
            insertPlayerDto(gameId,participant)
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
    createPlayerTable()
    start_index = 0
    amount = 1000
    while True :
        rows =selectParticipantIdentities(start_index,amount)
        c = len(rows)
        if c != 0 :
            savePlayers(rows)
            start_index+=amount
        else :
            break


