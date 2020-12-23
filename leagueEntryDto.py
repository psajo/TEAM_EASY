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


#데이터베이스에 LeagueEntry테이블 만들기
def createLeagueEntryTable() :
    # 데이터베이스 연결
    setConnCur()
    sql = 'CREATE TABLE IF NOT EXISTS leagueEntryDto ( \
    	leagueId CHAR(36), \
        summonerId VARCHAR(100), \
        summonerName VARCHAR(100), \
        queueType VARCHAR(20), \
        tier VARCHAR(20), \
        rank VARCHAR(3), \
        leaguePoints INT, \
        wins INT, \
        losses INT, \
        hotStreak BOOLEAN, \
        veteran BOOLEAN, \
        freshBlood BOOLEAN, \
        inactive BOOLEAN, \
        miniSeries VARCHAR(200) ,\
        apikey VARCHAR(50),\
        PRIMARY KEY(summonerName)\
    )'
    cur.execute(sql)
    conn.commit()
    print('create leagueEntry table.')
    closeConnCur()
#createLeagueEntryTable end


#leagueEntry테이블에 값 넣기
def insertLeagueEntry(response):
    print('response ',response)
    keys = list(response.keys())
    keys.append('apikey')
    values = list(response.values())
    values.append(api_key)
    p_list = ['%s' for _ in range(len(values))]
    for i,v in enumerate(values) :
        if type(v) == bool :
            values[i] = int(v)
        if type(v) == dict:
            values[i] = str(v)
    sql = 'REPLACE INTO leagueEntryDto('
    sql+=   ','.join(keys)
    sql+=   ') VALUES('
    sql+=   ','.join(p_list)
    sql+= ')'
    print(sql)
    cur.execute(sql,values)
    print('INSERT ',response['summonerName'])
    conn.commit()
#insertLeagueEntry end

#티어,단계로 소환사이름들 얻기
#https://kr.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/CHALLENGER/I?page=2
#TIER_LIST = ['CHALLENGER','GRANDMASTER','MASTER','DIAMOND','PLATINUM','GOLD','SILVER','BRONZE','IRON']
def saveLeagueEntries(tier,division,page=1,queue='RANKED_SOLO_5x5') :
    setConnCur()
    start_time = time.time()
    #uri = f'https://kr.api.riotgames.com/lol/league-exp/v4/entries/{queue}/{tier}/{division}?page={page}&api_key={API_KEY}'
    # headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    #     "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    #     "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    #     "Origin": "https://developer.riotgames.com",
    #     "X-Riot-Token": API_KEY
    # }
    count=0
    while True :
        uri = f'https://kr.api.riotgames.com/lol/league-exp/v4/entries/{queue}/{tier}/{division}?page={page}&api_key={api_key}'
        print(uri)
        response = requests.get(uri)
        status_code =response.status_code
        print('status_code : ',status_code)
        if status_code ==200 :
            leagueEntry_list = response.json()
            if leagueEntry_list :
                for leagueEntry in leagueEntry_list:
                    insertLeagueEntry(leagueEntry)
                #샘플데이터 받기 위해 2페이지만 나중에 지울것!
                if page >2 :
                    print('2page end')
                    break
                #여기까지 지울것!
                page += 1
            else :
                print(page,'page is end page!')
                break
        elif status_code == 429 :
            changeApikey()
            print('change API KEY. ', api_key)
            time.sleep(0.1)
        else :
            break;
        time.sleep(1)
        count += 1
        if count % 10 == 0:
            changeApikey()
            print('## change apikey. ', api_key)
    print(tier,division,' 작업시간 : %0.4f초'%(time.time()-start_time))
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
    createLeagueEntryTable()
    t =time.time()
    for i in range(len(TIER_LIST)) :
        for k in range(len(DIVISION_LIST)) :
            saveLeagueEntries(TIER_LIST[i],DIVISION_LIST[k])
    print('총 작업시간 : %.2f'%(time.time()-t))
