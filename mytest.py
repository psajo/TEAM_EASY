import pandas as pd
import mydao

class Test(mydao.MyDAO):
    def test(self) :
        self.connectDB()
        sql = 'select `key` from championdto'
        self.cur.execute(sql)
        rows =self.cur.fetchall()
        win_dictionary1 = {}
        for row in rows :
            sql = f"select count(*) from championdataset where (champion1='{row[0]}' or champion2='{row[0]}' or champion3='{row[0]}' or champion4='{row[0]}' or champion5='{row[0]}' or champion6='{row[0]}' or champion7='{row[0]}' or champion8='{row[0]}' or champion9='{row[0]}' or champion10='{row[0]}') AND win='1' "
            self.cur.execute(sql)
            rs =self.cur.fetchall()
            win_dictionary1[f'{row[0]}'] = rs[0][0]

        win_dictionary1 =sorted(win_dictionary1.items(), key=lambda x: x[1], reverse=True)
        print(win_dictionary1)
        lose_dictionary1 ={}
        for row in rows:
            sql = f"select count(*) from championdataset where (champion1='{row[0]}' or champion2='{row[0]}' or champion3='{row[0]}' or champion4='{row[0]}' or champion5='{row[0]}' or champion6='{row[0]}' or champion7='{row[0]}' or champion8='{row[0]}' or champion9='{row[0]}' or champion10='{row[0]}') AND win='0' "
            self.cur.execute(sql)
            rs = self.cur.fetchall()
            lose_dictionary1[f'{row[0]}'] = rs[0][0]

        lose_dictionary1 = sorted(lose_dictionary1.items(), key=lambda x: x[1], reverse=True)
        print(lose_dictionary1)


        self.closeDB()

if __name__ == '__main__':
    test = Test()
    test.test()
    # d ={}
    # d[1] =2
    # print(d)