import datetime

mydate =datetime.datetime.strptime('20201226', '%Y%m%d')
print(int(mydate.timestamp()))