from tensorflow.keras.layers import Dense, LSTM,Embedding,Bidirectional,Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.preprocessing import LabelEncoder
import dataSet

class MakeModels() :
    #lstm 모델을 만들고 학습시킨 후 h5로 저장한다
    def championid_bilstm_model(self):
        #데이터 로드
        ds = dataSet.DataSet()
        champs_df =ds.getChampions()
        df =ds.getChampionsDataSet()
        #챔피언아이디가 1~1000까지의 정수중에서 153개만 골라서 들어가 있기 때문에 153개의 숫자로 인코딩해준다
        le = LabelEncoder()
        le.fit(champs_df['key'])
        for i in range(len(df.columns)-1) :
            df.iloc[:,i] = le.transform(df.iloc[:,i])
        data = df.values

        #훈련,테스트 데이터 분리
        #수학적 표기법에서 벡터 변수는 소문자, 행렬 변수는 대문자 사용하는 관례가 있다고 한다. X,y로 표기함(y는 단일열 값이므로)
        row_count = len(data)  # 행의 수
        split_num = int(row_count * 0.8)  # 훈련,테스트를 8:2로 분리
        X_train = data[:split_num,:-1]
        y_train = data[:split_num,-1]
        X_test = data[split_num:, :-1]
        y_test = data[split_num:, -1]

        #모델 구성
        champ_size=153
        model = Sequential()
        model.add(Embedding(champ_size,100)) #챔피언 아이디가 최대 153, 100은 몇차원으로 벡터를 그릴건지이므로 변경가능
        model.add(Bidirectional(LSTM(153)))
        model.add(Dense(1, activation='softmax'))
        model.summary()
        #콜백함수 설정
        es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=5) #5번 연속 정확도가 떨어진다면 학습 종료
        mc = ModelCheckpoint('championid_bilstm_model.h5', monitor='val_acc', mode='max',
                             verbose=1, save_best_only=True) #정확도가 가장 좋은 가중치를 저장
        #하이퍼 파라미터 설정 - 최적화, 손실함수,평가방법 설정(정확도)
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])
        #모델 학습
        history = model.fit(X_train, y_train, epochs=20, callbacks=[es, mc], batch_size=8, validation_split=0.2)
        #ValueError: logits and labels must have the same shape ((None, 2) vs (None, 1))
        loaded_model = load_model('championid_bilstm_model.h5')
        print("\n 테스트 정확도: %.2f" % (loaded_model.evaluate(X_test, y_test)[1] * 100))

    def championTag_model(self):
        ds = dataSet.DataSet()
        df1 = ds.getChampTagDataSet()
        data = df1.values
        data = data.astype('float32')
        print('dtype : ',data.dtype)
        # 훈련,테스트 데이터 분리
        # 수학적 표기법에서 벡터 변수는 소문자, 행렬 변수는 대문자 사용하는 관례가 있다고 한다. X,y로 표기함(y는 단일열 값이므로)
        row_count = len(data)  # 행의 수
        split_num = int(row_count * 0.8)  # 훈련,테스트를 8:2로 분리
        print('split_num', split_num)
        X_train = data[:split_num, :-1]
        y_train = data[:split_num, -1]
        X_test = data[split_num:, :-1]
        y_test = data[split_num:, -1]

        # 모델 구성
        model = Sequential()
        model.add(Dense(400,input_dim=24, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(100,activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(1,activation='sigmoid'))
        model.summary()
        # 콜백함수 설정
        es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=5)  # 5번 연속 정확도가 떨어진다면 학습 종료
        mc = ModelCheckpoint('tag_dnn_model.h5', monitor='val_acc', mode='max',
                             verbose=1, save_best_only=True)  # 정확도가 가장 좋은 가중치를 저장
        # 하이퍼 파라미터 설정 - 최적화, 손실함수,평가방법 설정(정확도)
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])
        # 모델 학습
        history = model.fit(X_train, y_train, epochs=20, callbacks=[es, mc], batch_size=32, validation_split=0.2)
        # ValueError: logits and labels must have the same shape ((None, 2) vs (None, 1))
        loaded_model = load_model('tag_dnn_model.h5')
        print("\n 테스트 정확도: %.2f" % (loaded_model.evaluate(X_test, y_test)[1] * 100))

if __name__ == '__main__':
    mm = MakeModels()
    # mm.championid_bilstm_model()
    mm.championTag_model()