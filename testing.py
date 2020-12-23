import requests

url = 'http://ddragon.leagueoflegends.com/cdn/10.25.1/data/ko_KR/champion.json'
response =requests.get(url)
result =response.json()
data = result['data']
for value in data :
    print(data[value]['name'])