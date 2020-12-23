import pandas as pd
import pymysql

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

#챔피언 태그 데이터를 읽는다(탱커,지속딜,...)
def readChmpionTag() :
    df =pd.read_excel('Champion_Tag_psj.xlsx', sheet_name='Sheet1')
    return df

#한팀의 태그를 전체 합친다
def sumTeamTag(list1) :
    df = readChmpionTag()
    df.set_index('챔피언', inplace=True)
    team1 = df.loc[list1, :]
    print(team1)
    team1_stat = team1.sum()
    print('sum : ',team1_stat)
    return team1_stat

#두팀의 태그를 한 행으로 만든다
def getTeamAB(teamA,teamB) :
    teamA_tag =sumTeamTag(teamA)
    teamB_tag =sumTeamTag(teamB)
    teamAB_tag =pd.concat([teamA_tag,teamB_tag])
    df = pd.DataFrame(teamAB_tag)
    df = df.transpose()
    print('teamAB : ',df)
    return df

#sql 결과셋을 받아서(한게임, 참가자 10명) 학습시킬 데이터셋으로 변환
#gameId participantId championId winlose
def getDataset(rows):
    for row in rows :
        print(row)

#데이터베이스에서 한게임의 정보를 받아온다
def selectOneGame(gameId) :
    setConnCur()
    sql = 'SELECT * FROM participantDto WHERE gameId = %s'
    cur.execute(sql,gameId)
    rows =cur.fetchall()
    print('rows',rows)
    return rows

#전역변수들
# API_KEY = 'RGAPI-432cdf36-0e8c-418d-87d6-7d442b2de823' #주기적으로 갱신 해줘야됨
api_key=""; api_index =0
api_keys =[]
TIER_LIST = ['CHALLENGER','GRANDMASTER','MASTER','DIAMOND','PLATINUM','GOLD','SILVER','BRONZE','IRON'] #티어이름 내림차순
DIVISION_LIST = ['I','II','III','IV']
HOST='20.194.19.37'; PORT=3306; USER='te'; PASSWD='1234'; DB='teameasy'; CHARSET='utf8'
conn = None
cur = None

if __name__=="__main__" :

    teamA = ['아트록스','그레이브즈','애니비아','진','쓰레쉬']
    teamB = ['티모','마스터 이','나서스','베인','소라카']
    getTeamAB(teamA,teamB)
    rows = selectOneGame('4071423629')
    # getDataset(rows)