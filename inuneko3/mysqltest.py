import MySQLdb as my
 
#MariaDB connect
con = my.connect(user='root', password='mysql', database='inuneko3', use_unicode=True, charset="utf8")
cursor = con.cursor()
statement = "select * from sample"
cursor.execute(statement)
records = cursor.fetchall()
con.close()
print(records)