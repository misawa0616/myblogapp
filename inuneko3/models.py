from django.db import models
from django.utils import timezone

class Inuneko3(models.Model):
    inuneko3 = models.CharField(max_length=128)
    uploaded_at = models.DateTimeField(default=timezone.now)
    username = models.CharField(max_length=128)


'''
sqlコマンドで直接書きこむ場合
def InsertResult(result, Username):
	con = my.connect(user='root', password='mysql', database='myblogapp', use_unicode=True, charset="cp932")
	cursor = con.cursor()
	statement = "insert into inuneko3_inuneko3(inuneko3, uploaded_at, username) values (%s, now(), %s);"
	cursor.execute(statement, (result, Username, ))
	con.commit()
	cursor.close()
	con.close()

def SelectResult(Username):
	con = my.connect(user='root', password='mysql', database='myblogapp', use_unicode=True, charset="cp932")
	cursor = con.cursor()
	statement = "select inuneko3, uploaded_at from inuneko3_inuneko3 where username = %s ORDER BY id DESC limit 10;"
	cursor.execute(statement, (Username, ))
	rows = cursor.fetchall()
	cursor.close()
	con.close()
	return rows
'''
