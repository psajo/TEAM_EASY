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


#데이터베이스에 summoner테이블 만들기
def createSummonerTable() :
    # 데이터베이스 연결
    setConnCur()
    sql =   'CREATE TABLE IF NOT EXISTS summonerDto ( \
                accountId VARCHAR(100), \
                profileIconId INT, \
                revisionDate BIGINT, \
                name VARCHAR(100), \
                id VARCHAR(100), \
                puuid VARCHAR(100), \
                summonerLevel BIGINT, \
                apikey VARCHAR(50), \
                PRIMARY KEY(accountId)\
            )'
    cur.execute(sql)
    conn.commit()
    print('create summoner table.')
    closeConnCur()
#createSummonerTable end

#selectSummoner
def selectLeagueEntry(start=0, amount=1000) :
    setConnCur()
    sql = f'SELECT * FROM leagueEntryDto limit {start}, {amount}'
    cur.execute(sql)
    rows = cur.fetchall()
    closeConnCur()
    return rows
#selectSummoner end

#summoner테이블에 값 넣기
def insertSummoner(response):
    print('response ',response)
    keys = list(response.keys())
    keys.append('apikey')
    values = list(response.values())
    values.append(api_key)
    q_list = ['%s' for _ in range(len(values))]
    for i,v in enumerate(values) :
        if type(v) == bool :
            values[i] = int(v)
        if type(v) == dict:
            values[i] = str(v)
    sql = 'REPLACE INTO summonerDto('
    sql+=   ','.join(keys)
    sql+=   ') VALUES('
    sql+=   ','.join(q_list)
    sql+= ')'
    print(sql)
    cur.execute(sql,values)
    print('INSERT ',response['name'])
    conn.commit()
#insertLeagueEntry end

#티어,단계로 소환사이름들 얻기
#https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/hide%20on%20bush?api_key=RGAPI-c5b1b806-3cf1-4ff6-8e36-5174cb88f9f7
#TIER_LIST = ['CHALLENGER','GRANDMASTER','MASTER','DIAMOND','PLATINUM','GOLD','SILVER','BRONZE','IRON']
def saveSummoner(rows) :
    global api_key
    setConnCur()

    s_time = time.time() #시작시간
    p_time =time.time()  #과거 100개 완료된 시간
    count=0
    while count < len(rows)-1 :
        if (count+1) % 100 ==0 :
            print(count,'번째 까지 완료 ', time.time()-p_time,'초')
            p_time = time.time()
            time.sleep(1)
        summonerName = rows[count][2]
        uri = f'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}?api_key={api_key}'
        print(uri)
        response = requests.get(uri)
        status_code = response.status_code
        print('status_code : ', status_code)
        if status_code == 200:
            print()
            summoner = response.json()
            if summoner:
                insertSummoner(summoner)
                count += 1
                if count % 10 ==0 :
                    changeApikey()
        elif status_code == 429:
            print('## 사용량 제한 걸림. ',api_key)
            changeApikey()
            time.sleep(2)
            continue
        else:
            time.sleep(0.1)
        count +=1

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
    createSummonerTable()
    start_index =0
    amount =1000
    while True :
        rows =selectLeagueEntry(start_index,amount)
        c = len(rows)
        print('row 수 : ',c)
        if c != 0 :
            saveSummoner(rows)
            start_index +=amount
        else:
            break
