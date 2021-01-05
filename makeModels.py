from tensorflow.keras.layers import Dense, LSTM,Embedding
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import dataSet

class MakeModels() :
    #lstm 모델을 만들고 학습시킨 후 h5로 저장한다
    def lstm_model(self):
        #데이터 로드
        ds = dataSet.DataSet()
        df =ds.getChampionsDataSet()
        print(type(df))
        data = df.values

        #훈련,테스트 데이터 분리
        #수학적 표기법에서 벡터 변수는 소문자, 행렬 변수는 대문자 사용하는 관례가 있다고 한다. X,y로 표기함(y는 단일열 값이므로)
        row_count = len(data)  # 행의 수
        split_num = int(row_count * 0.8)  # 훈련,테스트를 8:2로 분리
        X_train = data[:split_num,:-1]
        y_train = data[:split_num,-1]
        X_test = data[split_num:, :-1]
        y_test = data[split_num:, -1]
        print(X_train.shape, y_train.shape, X_test.shape, y_test.shape)

        #모델 구성
        model = Sequential()
        model.add(Embedding(153, 100)) #챔피언 수 153명, 100은 몇차원으로 벡터를 그릴건지이므로 변경가능
        model.add(LSTM(100))
        model.add(Dense(2, activation='softmax'))
        model.summary()
        #콜백함수 설정
        es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=5) #5번 연속 정확도가 떨어진다면 학습 종료
        mc = ModelCheckpoint('best_lstm_model.h5', monitor='val_acc', mode='max',
                             verbose=1, save_best_only=True) #정확도가 가장 좋은 가중치를 저장
        #하이퍼 파라미터 설정 - 최적화, 손실함수,평가방법 설정(정확도)
        model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])
        #모델 학습
        history = model.fit(X_train, y_train, epochs=20, callbacks=[es, mc], batch_size=1000, validation_split=0.2) ##데이터셋 구성 다시 해야됨
        #ValueError: logits and labels must have the same shape ((None, 2) vs (None, 1))
        loaded_model = load_model('best_model.h5')
        print("\n 테스트 정확도: %.4f" % (loaded_model.evaluate(X_test, y_test)[1]))

    #rnn모델을 만들고 학습시킨 후 h5로 저장한다
    def rnn_model(self):
        pass

if __name__ == '__main__':
    mm = MakeModels()
    mm.lstm_model()