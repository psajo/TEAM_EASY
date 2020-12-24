import requests
import pymysql
import time


# APIKEY파일에서 읽기
def setApikey():
    global api_keys, api_key
    with open('C:/Users/kccistc/Desktop/apikey.txt', 'r') as f:
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

'''
CREATE TABLE IF NOT EXISTS `mydb`.`champion` (
  `version` VARCHAR(20) NOT NULL,
  `id` VARCHAR(20) NULL,
  `key` INT NOT NULL,
  `name` VARCHAR(50) NULL,
  `title` VARCHAR(50) NULL,
  `blurb` VARCHAR(1000) NULL,
  `info` JSON NULL,
  `image` JSON NULL,
  `tags` JSON NULL,
  `partype` VARCHAR(20) NULL,
  `stats` JSON NULL,
  PRIMARY KEY (`key`, `version`))
ENGINE = InnoDB
'''
# 데이터베이스에 champions테이블 만들기
def createChampionTable():
    # 데이터베이스 연결
    setConnCur()
    sql = 'CREATE TABLE IF NOT EXISTS `champion`('
    sql+=   '`version` VARCHAR(20) NULL,'
    sql+=   '`id` VARCHAR(20) NULL,'
    sql+=   '`key` INT NOT NULL,'
    sql +=  '`name` VARCHAR(50) NULL,'
    sql +=  '`title` VARCHAR(50) NULL,'
    sql +=  '`blurb` VARCHAR(1000) NULL,'
    sql +=  '`info` JSON NULL,'
    sql +=  '`image` JSON NULL,'
    sql +=  '`tags` JSON NULL,'
    sql +=  '`partype` VARCHAR(20) NULL,'
    sql +=  '`stats` JSON NULL,'
    sql+=   'PRIMARY KEY (`version`,`key`)'
    sql+= ')'
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

#mysql json_object형식으로 만들어주기
def transformForDB(val) :
    if type(val) == list :
        return ','.join(val)
    elif type(val) == dict :
        val_keys =val.keys()
        val_values = val.values()
        ret_str = ''
        list1 = []
        for k,v in zip(val_keys,val_values) :
            if type(v) == int :
                list1.append(f'"{k}",{v}')
            else :
                list1.append(f'"{k}","{v}"')
        ret_str = ','.join(list1)
        print('#json_object(',ret_str,')')
        return ret_str
    elif type(val) == bool:
        return int(val)
    else :
        return val

# champion 테이블에 여러값 넣기
def insertChampions():
    setConnCur()
    uri = 'http://ddragon.leagueoflegends.com/cdn/10.25.1/data/ko_KR/champion.json'
    response =requests.get(uri)
    data =response.json()['data']
    for champ in data :
        keys = data[champ].keys()
        keys = [ f'`{k}`' for k in keys ] #예약어랑 겹칠 수도 있기 때문에 문자열로 만들어준다
        values = list(data[champ].values())
        p_list = []
        for v in values :
            if type(v) == dict:
                p_list.append('json_object(%s)')
            else :
                p_list.append('%s')
        for i,e in enumerate(values) :
            values[i] = transformForDB(e)
        print('testing : ',values)
        sql = 'INSERT INTO champion('
        sql += ','.join(keys)
        sql += ') VALUES('
        sql += ','.join(p_list)
        sql += ')'
        print(sql)
        print('값 :',values)
        cur.execute(sql,values)
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
HOST = 'localhost';
PORT = 3306;
USER = 'root';
PASSWD = '1234';
DB = 'team_easy';
CHARSET = 'utf8'
conn = None
cur = None

if __name__ == '__main__':
    createChampionTable()
    insertChampions()