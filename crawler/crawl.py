#coding=utf-8

import re
import requests
import urllib
import sys
import datetime as dt
from datetime import datetime
import time
from bs4 import BeautifulSoup
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf-8')

today = datetime.now()
lastthreedays = today - dt.timedelta(days = 90)
category = ['人事信息', '政府采购', '资质认证', '未分类项']

db = MySQLdb.connect('localhost', 'root', 'root', 'honey', charset='utf8')
cursor = db.cursor()

def guangdong_solution(li):
	province = '广东'
	root = 'http://www.gdlr.gov.cn'
	response = requests.get(li[1])
	response.encoding = 'utf-8'
	data = response.text
	bf = BeautifulSoup(data, 'lxml')
	lt = bf.find_all('div', class_='list')[1]
	lt = lt.find_all('ul')[0]
	lt = lt.find_all('li')
	for i in range(0, len(lt)):
		line = lt[i]
		date = line.find_all('div', class_='Date')[0]
		date = date.get_text().replace('\t', '').replace(' ', '').replace('\n', '')
		date = datetime.strptime(date, '%Y-%m-%d')
		if date > today or date < lastthreedays:
			continue
		link = line.find_all('a')[0]
		desp = link.get('title')
		url = root + link.get('href')
		try:
			pre_sql = "select * from current where url = '%s'" % url
			if cursor.execute(pre_sql) == 0:
				sql = "insert into current(type, description, dt, url, province, part) \
				values ('%d', '%s', '%s', '%s', '%s', '%s')" \
				% (li[0], desp, date, url, province, li[2])
				cursor.execute(sql)
			db.commit()
		except Exception as e:
		    print e
		    db.rollback()

def guangdong():
	url = [
			[0, 'http://www.gdlr.gov.cn/gdsgtzyt/_132477/_132509/index.html', '人事任免'],
			[0, 'http://www.gdlr.gov.cn/gdsgtzyt/_132477/_132513/index.html', '公务员考录'],
			[0, 'http://www.gdlr.gov.cn/gdsgtzyt/_132477/_132517/index.html', '事业单位招聘'],
			[2, 'http://www.gdlr.gov.cn/gdsgtzyt/_132477/_132501/_134132/_134156/_134168/index.html', '矿业权评估'],
	]
	for li in url:
		guangdong_solution(li)
		time.sleep(17)

guangdong()
db.close()

def jiangsu_renshi():

	url = ['http://www.jsmlr.gov.cn/gtxxgk/nrglIndex.action?classID=8a908254409a391f01409a4b6d38000a'
, '江苏人事任免']
	root = 'http://www.jsmlr.gov.cn'
	response = requests.get(url[0])
	response.encoding = 'GBK'
	data = response.text
	print data

	data = open('a.out', 'r').read()

	bf = BeautifulSoup(data, 'lxml')
	tb = bf.find_all('table')[0].find_all('table')[0]
	lt = bf.find_all('div', class_='list')[1]
	lt = lt.find_all('ul')[0]
	lt = lt.find_all('li')
	for i in range(0, len(lt)):
		line = lt[i]
		date = line.find_all('div', class_='Date')[0]
		date = date.get_text().replace('\t', '').replace(' ', '').replace('\n', '')
		date = datetime.strptime(date, '%Y-%m-%d')
		if date > today or date < lastthreedays:
			continue
		link = line.find_all('a')[0]
		return '<div>' + \
		 	'<p>' + url[1] + '</p>' + \
			'<a href=\"' + root + link.get('href') + '\">' + link.get('title') + '</a>' + \
			'</div>'
