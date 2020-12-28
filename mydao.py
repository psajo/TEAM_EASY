import pymysql
#데이터베이스에 접근하는 기본 클래스
class MyDAO:
    HOST = 'localhost';
    PORT = 3306;
    USER = 'root';
    PASSWD = '1234';
    DB = 'team_easy';
    CHARSET = 'utf8'
    conn = None
    cur= None

    #데이터베이스 접속 정보를 설정한다
    def setCfg(self,HOST,PORT,USER,PASSWD,DB,CHARSET):
        self.HOST = HOST
        self.PORT = PORT
        self.USER = USER
        self.PASSWD = PASSWD
        self.DB = DB
        self.CHARSET = CHARSET

    #접속정보를 가지고 데이터베이스에서 커넥션과 커서를 얻어 저장한다
    def connectDB(self):
        self.conn = pymysql.connect(host=self.HOST, port=self.PORT, user=self.USER, passwd=self.PASSWD, db=self.DB, charset=self.CHARSET)
        self.cur = self.conn.cursor()

    #커넥션과 커서 자원 해제
    def closeDB(self):
        self.cur.close()
        self.conn.close()

    #dictionary, list를 문자열로, bool을 tinyint로
    def transformForDB(self,val):
        if type(val) == list:
            return ','.join(val)
        elif type(val) == dict:
            return str(val).replace('\'', '\"')
        elif type(val) == bool:
            return int(val)
        else:
            return val


