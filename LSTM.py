from numpy import array
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import pandas as pd
# 1. 데이터
import mydao
import collectData
import ast
class Test(mydao.MyDAO, collectData.CollectData) :
    def extractJson(self) :
        self.connectDB()
        #gameId = 3479309056
        sql = 'SELECT gameId,teams,participants FROM matchDto LIMIT 0, 1000'
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        self.closeDB()
        return rows
test = Test()
rows =test.extractJson()
rows2 = []
for row in rows :
    gameId =row[0]
    teams = ast.literal_eval( row[1])
    participants = ast.literal_eval( row[2])
    temp = [participants[0]['championId'], participants[1]['championId'], participants[2]['championId'],
            participants[3]['championId'], participants[4]['championId'], participants[5]['championId'], participants[6]['championId']
            , participants[7]['championId'], participants[8]['championId'], participants[9]['championId'],
            1 if teams[0]['win']=='Win' else 0]
    rows2.append(temp)

df1 = pd.DataFrame(rows2, columns=['champion1','champion2','champion3','champion4',
                                  'champion5','champion6','champion7','champion8','champion9','champion10','win'])
values = df1.values
x_train = values[:800,:-1]
y_train = values[:800,-1]
x_test = values[800:, :-1]
y_test = values[800:, -1]
print(x_train.shape, y_train.shape)
x_train =x_train.reshape(x_train.shape[0],x_train.shape[1],1)
x_test = x_test.reshape(x_test.shape[0],x_test.shape[1],1)
# 2. 모델 구성
model = Sequential()
model.add(LSTM(10, activation='relu', input_shape=(10, 1)))
# DENSE와 사용법 동일하나 input_shape=(열, 몇개씩잘라작업)
model.add(Dense(5))
model.add(Dense(1,activation='sigmoid'))
model.summary()
# 3. 실행
model.compile(optimizer='adam', loss='mse',metrics=['accuracy'])
model.fit(x_train, y_train, epochs=100, batch_size=128)
score, acc = model.evaluate(x_test, y_test, batch_size=32)
print('## evaluation loss and_metrics ##')
print(score, acc)
# x = array([[1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]])
# y = array([4, 5, 6, 7])
#
# print('x shape : ', x.shape)  # (4,3)
# print('y shape : ', y.shape)  # (4,)
# #  x  y
# # 123 4
# # 234 5
# # 345 6
# # 456 7
#
# print(x)
# print('-------x reshape-----------')
# x = x.reshape((x.shape[0], x.shape[1], 1))  # (4,3,1) reshape 전체 곱 수 같아야 4*3=4*3*1
# print('x shape : ', x.shape)
# print(x)
# #  x        y
# # [1][2][3] 4
# # .....
#
# # 2. 모델 구성
# model = Sequential()
# model.add(LSTM(10, activation='relu', input_shape=(3, 1)))
# # DENSE와 사용법 동일하나 input_shape=(열, 몇개씩잘라작업)
# model.add(Dense(5))
# model.add(Dense(1))
#
# model.summary()
#
# # 3. 실행
# model.compile(optimizer='adam', loss='mse')
# model.fit(x, y, epochs=100, batch_size=1)
#
# x_input = array([6, 7, 8])
# x_input = x_input.reshape((1, 3, 1))
#
# yhat = model.predict(x_input)
# print(yhat)