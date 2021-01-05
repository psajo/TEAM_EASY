from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from numpy import array
import dataSet

class MakeModels() :
    #lstm 모델을 만들고 학습시킨 후 h5로 저장한다
    def lstm_model(self):
        #데이터 로드
        ds = dataSet.DataSet()
        df =ds.getChampionsDataSet()
        print(df.head(5))
        #모델 구성
        model = Sequential()
        model.add(LSTM(10, activation='relu', input_shape=(10, )))
        # DENSE와 사용법 동일하나 input_shape=(열, 몇개씩잘라작업)
        model.add(Dense(5))
        model.add(Dense(1))
        model.summary()
    #rnn모델을 만들고 학습시킨 후 h5로 저장한다
    def rnn_model(self):
        pass

if __name__ == '__main__':
    mm = MakeModels()
    mm.lstm_model()