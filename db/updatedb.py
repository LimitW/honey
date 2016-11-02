#coding=utf-8
import re
import requests
import urllib
import sys
import datetime as dt
from datetime import date
import time
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf-8')

def _del():
	try:
		pre_sql = "select url from history where dt = '%s'" % today
		cursor.execute(pre_sql)
		res = cursor.fetchall()
		for i in range(0, len(res)):
			sql = "delete from current where status = 1 and url = '%s'" % (res[i][0])
			cursor.execute(sql)
		db.commit()
	except Exception as e:
	    print e
	    db.rollback()

def _update():
	try:
		pre_sql = "select type, description, url, province, part from current where status = 1"
		cursor.execute(pre_sql)
		res = cursor.fetchall()
		for i in range(0, len(res)):
			sql = "insert into history(type, description, dt, url, province, part) \
				values ('%d', '%s', '%s', '%s', '%s', '%s')" \
				% (res[i][0], res[i][1], today, res[i][2], res[i][3], res[i][4])
			cursor.execute(sql)
		db.commit()
		_del()
	except Exception as e:
	    print e
	    db.rollback()

db = MySQLdb.connect('localhost', 'root', 'root', 'honey', charset='utf8')
cursor = db.cursor()
today = date.today()
_update()
db.close()

print today, 'update done'
