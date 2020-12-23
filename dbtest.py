import pymysql

# Open database connection
db = pymysql.connect(host='20.194.19.37', port=3306, user='te', passwd='1234', db='teameasy', charset='utf8')

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()

print("Database version : %s " % data)

# disconnect from server
db.close()
