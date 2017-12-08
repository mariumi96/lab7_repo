import MySQLdb
from MySQLdb.constants import FIELD_TYPE

db = MySQLdb.connect(host="localhost", db="ask_db", user="dbuser", passwd="123", charset='utf8')
cursor=db.cursor()
cursor.execute("select * from ask_question")
result = cursor.fetchall()

for x in result:
    print(x)
