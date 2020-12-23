import requests
import pymysql
import time


# APIKEY파일에서 읽기
def setApikey():
    global api_keys, api_key
    with open('C:/Users/psajo/Desktop/apikey.txt', 'r') as f:
        api_keys = f.read().split()
    print('api_key리스트 : ', api_keys)
    api_key = api_keys[api_index]


# APIKEY 바꾸기
def changeApikey(key=""):
    global api_index, api_key
    if key != "":  # 입력값이 있으면
        api_key = key
    else:  # 입력값이 없으면
        max_index = len(api_keys)
        api_index = api_index + 1
        if api_index > max_index - 1:  # index넘어갔을때
            api_index = 0
        print('api_index', api_index)
        api_key = api_keys[api_index]


# conn, cur 얻기
def setConnCur():
    global conn, cur
    conn = pymysql.connect(host=HOST, port=PORT, user=USER, passwd=PASSWD, db=DB, charset=CHARSET)
    cur = conn.cursor()


# conn, cur 닫기
def closeConnCur():
    conn.commit()
    cur.close()
    conn.close()


# 데이터베이스에 champions테이블 만들기
def createChampionsTable():
    # 데이터베이스 연결
    setConnCur()
    sql = 'CREATE TABLE IF NOT EXISTS champions('
    sql += 'championId INT, '
    sql += 'championName VARCHAR(20), '
    sql += 'championNameKR VARCHAR(20),'
    sql += 'PRIMARY KEY(championId)'
    sql += ')'
    print(sql)
    cur.execute(sql)
    conn.commit()
    print('create champions table.')
    closeConnCur()
# createChampionsTable end ####

#champion Tag 테이블 만들기
def champTag() :
    setConnCur()
    sql = 'CREATE TABLE IF NOT EXISTS champTag('
    sql+=   'championId INT, '
    sql+=   'championTag VARCHAR('

# match테이블에 값 넣기
def insertChampions():
    setConnCur()
    uri = 'http://ddragon.leagueoflegends.com/cdn/10.25.1/data/ko_KR/champion.json'
    response =requests.get(uri)
    data =response.json()['data']
    for champ in data :
        champName = data[champ]['id']
        champId = data[champ]['key']
        champNameKR = data[champ]['name']
        sql = 'REPLACE INTO champions('
        sql += 'championId, championName, championNameKR'
        sql += ') VALUES('
        sql += f'{champId}, "{champName}", "{champNameKR}"'
        sql += ')'
        print(sql)
        cur.execute(sql)
        conn.commit()
    closeConnCur()
# insertChampions end



# 전역변수들
# API_KEY = 'RGAPI-432cdf36-0e8c-418d-87d6-7d442b2de823' #주기적으로 갱신 해줘야됨
api_key = "";
api_index = 0
api_keys = []
TIER_LIST = ['CHALLENGER', 'GRANDMASTER', 'MASTER', 'DIAMOND', 'PLATINUM', 'GOLD', 'SILVER', 'BRONZE',
             'IRON']  # 티어이름 내림차순
DIVISION_LIST = ['I', 'II', 'III', 'IV']
HOST = '20.194.19.37';
PORT = 3306;
USER = 'te';
PASSWD = '1234';
DB = 'teameasy';
CHARSET = 'utf8'
conn = None
cur = None

if __name__ == '__main__':
    createChampionsTable()
    insertChampions()
