#api를 사용하는데 있어 기본적인 클래스
class CollectData :
    api_key = ""
    api_index = 0
    api_keys = []
    TIER_LIST = ['CHALLENGER', 'GRANDMASTER', 'MASTER', 'DIAMOND', 'PLATINUM', 'GOLD', 'SILVER', 'BRONZE',
                 'IRON']  # 티어이름 내림차순
    DIVISION_LIST = ['I', 'II', 'III', 'IV']

    # APIKEY파일에서 읽기
    #path='C:/Users/psajo/Desktop/apikey.txt'
    def setApikeyFromFile(self,path='apikey.txt'):
        with open(path, 'r') as f:
            self.api_keys = f.read().split()
        print('api_key리스트 : ', self.api_keys)
        self.api_key = self.api_keys[self.api_index]

    # APIKEY 바꾸기
    def changeApikey(self,key=""):
        if key != "":  # 입력값이 있으면
            self.api_key = key
        else:  # 입력값이 없으면
            max_index = len(self.api_keys) -1
            self.api_index = self.api_index + 1
            if self.api_index > max_index :  # index넘어갔을때
                self.api_index = 0
            print('api index : ',self.api_index)
            self.api_key = self.api_keys[self.api_index]
            print('api key : ',self.api_key)
