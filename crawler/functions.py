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
lastthreedays = today - dt.timedelta(days = 1)
category = ['人事信息', '政府采购', '资质认证', '未分类项']

def write_to_db(li, desp, url, province, date):
	db = MySQLdb.connect('localhost', 'root', 'root', 'honey', charset='utf8')
	cursor = db.cursor()
	try:
		pre_sql = "select * from current where url = '%s'" % url
		pre_sql2 = "select * from history where url = '%s'" % url
		if cursor.execute(pre_sql) == 0 and cursor.execute(pre_sql2) == 0:
			sql = "insert into current(type, description, dt, url, province, part) \
			values ('%d', '%s', '%s', '%s', '%s', '%s')" \
			% (li[0], desp, date, url, province, li[2])
			cursor.execute(sql)
		db.commit()
	except Exception as e:
	    print e
	    db.rollback()
	db.close()

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
		write_to_db(li, desp, url, province, date)
	print '广东' + li[2] + 'done'

def guangdong():
	url = [
			[0, 'http://www.gdlr.gov.cn/gdsgtzyt/_132477/_132509/index.html', '人事任免'],
			[0, 'http://www.gdlr.gov.cn/gdsgtzyt/_132477/_132513/index.html', '公务员考录'],
			[0, 'http://www.gdlr.gov.cn/gdsgtzyt/_132477/_132517/index.html', '事业单位招聘'],
			[2, 'http://www.gdlr.gov.cn/gdsgtzyt/_132477/_132501/_134132/_134156/_134168/index.html', '矿业权评估'],
	]
	for li in url:
		try:
			guangdong_solution(li)
		except Exception as e:
			print e
			continue
		if li != url[-1]:
			time.sleep(7)

def anhui_solution(li):
	province = '安徽'
	root = 'http://www.ahgtt.gov.cn/zwgk'
	response = requests.get(li[1])
	response.encoding = 'GBK'
	data = response.text
	bf = BeautifulSoup(data,'html.parser')
	tb = bf.find('table', attrs={"style":"margin-top:12px;"})
	lt = tb.find_all('tr', recursive=False)
	for i in range(0, len(lt)):
		if i % 2 != 0:
			continue
		line = lt[i]
		line = line.find_all('td', recursive=False)
		date = line[-1].get_text().encode('utf-8')
		date = datetime.strptime(date, '%Y-%m-%d')
		if date > today or date < lastthreedays:
			continue
		a_tag = line[0].find_all('a', 'k5')[0]
		url = root + a_tag.get('href')
		desp = a_tag.get_text()
		write_to_db(li, desp, url, province, date)
	print '安徽' + li[2] + 'done'

def anhui():
	url = [
		[1, 'http://www.ahgtt.gov.cn/zwgk/gkml.jsp?showtype=1&cat_rowid=080200', '招标信息'],
		[1, 'http://www.ahgtt.gov.cn/zwgk/gkml.jsp?showtype=1&cat_rowid=080300', '中标信息'],
		[0, 'http://www.ahgtt.gov.cn/zwgk/gkml.jsp?showtype=1&cat_rowid=030000', '人事信息']
	]
	for li in url:
		try:
			anhui_solution(li)
		except Exception as e:
			print e
			continue
		if li != url[-1]:
			time.sleep(7)

def hunan_solution(li):
	province = '湖南'
	response = requests.get(li[1])
	response.encoding = 'utf-8'
	data = response.text
	bf = BeautifulSoup(data, 'lxml')
	lt = bf.find_all('div', 'wenjian_3')
	lts = []
	for i in range(0, len(lt)):
		lt[i] = lt[i].find_all('li')
		for j in range(0, len(lt[i])):
			lts.append(lt[i][j])
	root = li[1]
	for i in range(0, len(lts)):
		line = lts[i]
		date = line.find_all('span')[0].get_text()
		date = datetime.strptime(date, '%Y-%m-%d')
		if date > today or date < lastthreedays:
			continue
		a_tag = line.find_all('a')[0]
		url = root + a_tag.get('href')[2:]
		desp = a_tag.get('title')
		write_to_db(li, desp, url, province, date)
	print province + li[2] + 'done'

def hunan():
	url = [
		[0, 'http://www.gtzy.hunan.gov.cn/gtmh/zwgk/rsxx/', '人事信息'],
		[1, 'http://www.gtzy.hunan.gov.cn/gtmh/zwgk/zfcg/zbxx/', '中标信息'],
		[1, 'http://www.gtzy.hunan.gov.cn/gtmh/zwgk/zfcg/cgzb/', '招标信息'],
		[3, 'http://www.gtzy.hunan.gov.cn/gtmh/zwgk/gsgg/', '通知公告']
	]
	for li in url:
		try:
			hunan_solution(li)
		except Exception as e:
			print e
			continue
		if li != url[-1]:
			time.sleep(7)

def yunnan_solution(li):
	province = '云南'
	response = requests.get(li[1])
	response.encoding = 'gb2312'
	data = response.text
	bf = BeautifulSoup(data, 'lxml')
	lt = bf.find_all('div', 'colcont')[0]
	lts = lt.find_all('li')
	root = 'http://www.yndlr.gov.cn/'
	for i in range(0, len(lts)):
		line = lts[i]
		date = line.find_all('span')[0].get_text()
		date = datetime.strptime(date, '%Y-%m-%d')
		if date > today or date < lastthreedays:
			continue
		a_tag = line.find_all('a')[0]
		url = root + a_tag.get('href')
		desp = a_tag.get('title')
		write_to_db(li, desp, url, province, date)
	print province + li[2] + 'done'

def yunnan():
	url = [
		[1, 'http://www.yndlr.gov.cn/newslist.aspx?depid=1&classid=6791', '招标信息'],
		[1, 'http://www.yndlr.gov.cn/newslist.aspx?depid=1&classid=6913', '中标信息'],
		[2, 'http://www.yndlr.gov.cn/newslist.aspx?depid=1&classid=6176', '矿业权评估']
	]
	for li in url:
		try:
			yunnan_solution(li)
		except Exception as e:
			print e
			continue
		if li != url[-1]:
			time.sleep(7)

def shandong_solution(li):
	province = '山东'
	response = requests.get(li[1])
	response.encoding = 'utf-8'
	data = response.text
	bf = BeautifulSoup(data, 'lxml')
	lt = bf.find_all('div', 'list01')[0]
	lts = lt.find_all('li')
	root = 'http://www.sddlr.gov.cn/'
	for i in range(0, len(lts)):
		line = lts[i]
		date = line.find_all('span')[0].get_text()
		date = datetime.strptime(date, '%Y-%m-%d')
		if date > today or date < lastthreedays:
			continue
		a_tag = line.find_all('a')[0]
		url = root + a_tag.get('href')[9:]
		desp = a_tag.get_text()
		write_to_db(li, desp, url, province, date)
	print province + li[2] + 'done'

def shandong():
	url = [
		[0, 'http://www.sddlr.gov.cn/zwgk/cehui/qita/', '人事任免'],
		[0, 'http://www.sddlr.gov.cn/zwgk/cehui/zhengce/', '人员考录'],
		[3, 'http://www.sddlr.gov.cn/zwgk/xuke/chufa/', '通知公告']
	]
	for li in url:
		try:
			shandong_solution(li)
		except Exception as e:
			print e
			continue
		if li != url[-1]:
			time.sleep(7)

def jiangsu_solution(li):
	province = '江苏'
	response = requests.get(li[1])
	response.encoding = 'GBK'
	data = response.text
	bf = BeautifulSoup(data, 'html.parser')
	root = 'http://www.jsmlr.gov.cn'
	if li[0] == 0:
		tb = bf.find_all('table', attrs={"border":"1"})[0].find_all('tbody')[0]
	else:
		tb = bf.find_all('table', attrs={"width":"98%"})[0]
	lts = tb.find_all('tr', recursive=False)
	for i in range(0, len(lts)):
		line = lts[i]
		date = line.find_all('td')[-1].get_text()
		date = datetime.strptime(date, '%Y-%m-%d')
		if date > today or date < lastthreedays:
			continue
		a_tag = line.find_all('a')[0]
		desp = a_tag.get('title') if li[0] else a_tag.get_text()[1:]
		url = a_tag.get('href') if li[0] else root + a_tag.get('href')
		write_to_db(li, desp, url, province, date)
	print province + li[2] + 'done'

def jiangsu():
	url = [
		[0, 'http://www.jsmlr.gov.cn/gtxxgk/nrglIndex.action?classID=8a908254409a391f01409a4b6d38000a', '人事信息'],
		[3, 'http://www.jsmlr.gov.cn/gggs/', '通知公告']
	]
	for li in url:
		try:
			jiangsu_solution(li)
		except Exception as e:
			print e
			continue
		if li != url[-1]:
			time.sleep(7)

def guangxi_solution(li):
	province = '广西'
	response = requests.get(li[1])
	response.encoding = 'gb2312'
	data = response.text
	bf = BeautifulSoup(data, 'html.parser')
	root = 'http://www.gxdlr.gov.cn/news/'
	reg = re.compile(r'[0-9\-]+')
	if li[0] != 0:
		tb = bf.find_all('table', id='ContentPlaceHolder1_GridView1')[0]
		lts = tb.find_all('td')
		for i in range(0, len(lts)):
			line = lts[i]
			div = line.find_all('div', recursive=False)
			if len(div) != 1:
				continue
			divs = div[0].find_all('div')
			if len(divs) != 3:
				continue
			date = divs[-1].get_text()
			date = '20' + reg.search(date).group(0)
			date = datetime.strptime(date, '%Y-%m-%d')
			if date > today or date < lastthreedays:
				continue
			a_tag = divs[1].find_all('a')[0]
			desp = a_tag.get('title')
			url = root + a_tag.get('href')
			write_to_db(li, desp, url, province, date)
	else:
		lts = bf.find_all('div', attrs={"style": "font-size:12px; line-height:20px; width:600px;"})
		for i in range(0, len(lts)):
			line = lts[i]
			date = line.find_all('div', recursive=False)[-1].get_text()
			date = '2016-' + reg.search(date).group(0)
			date = datetime.strptime(date, '%Y-%m-%d')
			if date > today or date < lastthreedays:
				continue
			a_tag = line.find_all('a')[0]
			desp = a_tag.get('title')
			url = root + a_tag.get('href')
			write_to_db(li, desp, url, province, date)
	print province + li[2] + 'done'

def guangxi():
	url = [
		[0, 'http://www.gxdlr.gov.cn/News/NewsList.aspx?ParentId=6', '人事信息'],
		[1, 'http://www.gxdlr.gov.cn/news/NewsClassList.aspx?ParentId=31&ClassId=155', '招投标信息'],
		[3, 'http://www.gxdlr.gov.cn/news/NewsClassList.aspx?ParentId=31&ClassId=153', '本厅通知'],
		[3, 'http://www.gxdlr.gov.cn/news/NewsClassList.aspx?ParentId=31&ClassId=154', '公告公示']
	]
	for li in url:
		try:
			guangxi_solution(li)
		except Exception as e:
			print e
			continue
		if li != url[-1]:
			time.sleep(7)

def henan_solution(li):
	province = '河南'
	response = requests.get(li[1])
	response.encoding = 'utf-8'
	data = response.text
	bf = BeautifulSoup(data, 'html.parser')
	root = 'http://www.hnblr.gov.cn/'
	tb = bf.find_all('div', 'gtrightxx')[0].find_all('div')[0]
	lts = tb.find_all('div', recursive=False)
	reg = re.compile(r'[0-9\-]*')
	for i in range(0, len(lts)):
		line = lts[i]
		date_div = line.find_all('div', 'xxlbdatecon')
		if len(date_div) != 1:
			continue
		date = date_div[0].get_text()
		date = reg.search(date).group(0)
		date = datetime.strptime(date, '%Y-%m-%d')
		if date > today or date < lastthreedays:
			continue
		a_tag = line.find_all('a')[0]
		desp = a_tag.get_text().replace('\r', '').replace('\n', '').replace('\t','')
		url = root + a_tag.get('href')
		write_to_db(li, desp, url, province, date)
	print province + li[2] + 'done'

def henan():
	url = [
		[0, 'http://www.hnblr.gov.cn/viewCmsCac.do?cacId=ff8080814d40886d014d425b0e680021','人事信息'],
		[1, 'http://www.hnblr.gov.cn/viewCmsCac.do?cacId=ff8080814d40886d014d425b0e5c001f', '政府采购'],
		[3, 'http://www.hnblr.gov.cn/viewCmsCac.do?cacId=ff8080814d40886d014d425b0e57001e', '通知公告']
	]
	for li in url:
		try:
			henan_solution(li)
		except Exception as e:
			print e
			continue
		if li != url[-1]:
			time.sleep(7)

def guizhou_solution(li):
	province = '贵州'
	response = requests.get(li[1])
	response.encoding = 'gb2312'
	data = response.text
	bf = BeautifulSoup(data, 'html.parser')
	root = 'http://www.gzgtzy.gov.cn'
	a_lts = bf.find_all('a', 'ListsLink')
	date_lts = bf.find_all('td', 'ListsDate')
	if len(a_lts) != len(date_lts):
		print '贵州class长度不匹配'
		return
	for i in range(0, len(a_lts)):
		date = '20' + date_lts[i].get_text()[0:8]
		date = datetime.strptime(date, '%Y-%m-%d')
		if date > today or date < lastthreedays:
			continue
		a_tag = a_lts[i]
		desp = a_tag.get_text()
		url = root + a_tag.get('href')
		write_to_db(li, desp, url, province, date)
	print province + li[2] + 'done'

def guizhou():
	url = [
		[0, 'http://www.gzgtzy.gov.cn/Html/Sort/Sort20/index.html','人事任免'],
		[3, 'http://www.gzgtzy.gov.cn/Html/Sort/Sort5/index.html', '通知公告']
	]
	for li in url:
		try:
			guizhou_solution(li)
		except Exception as e:
			print e
			continue
		if li != url[-1]:
			time.sleep(7)

def ningxia_solution(li):
	province = '宁夏'
	response = requests.get(li[1])
	response.encoding = 'utf-8'
	data = response.text
	bf = BeautifulSoup(data, 'html.parser')
	root = 'http://www.nxgtt.gov.cn'
	tb = bf.find_all('table', 'winstyle715444835_1196')[0]
	lts = tb.find_all('tr', recursive=False)
	reg = re.compile(r'[0-9\/]+')
	for i in range(0, len(lts)):
		line = lts[i]
		if len(line.find_all('td', recursive=False)) != 3:
			continue
		date = line.find_all('span', 'timestyle715444835_1196')[0].get_text()
		date = reg.search(date).group(0)
		date = datetime.strptime(date, '%Y/%m/%d')
		if date > today or date < lastthreedays:
			continue
		a_tag = line.find_all('a')[0]
		desp = a_tag.get('title')
		url = root + a_tag.get('href')
		write_to_db(li, desp, url, province, date)
	print province + li[2] + 'done'

def ningxia():
	url = [
		[0, 'http://www.nxgtt.gov.cn/ZW_RSXX_List.jsp?urltype=tree.TreeTempUrl&wbtreeid=1053', '人事信息'],
		[1, 'http://www.nxgtt.gov.cn/ZW_ZWXX_List.jsp?urltype=tree.TreeTempUrl&wbtreeid=1382', '招拍挂信息']
	]
	for li in url:
		try:
			guizhou_solution(li)
		except Exception as e:
			print e
			continue
		if li != url[-1]:
			time.sleep(7)

def hainan_solution(li):
	province = '海南'
	response = requests.get(li[1])
	response.encoding = 'utf-8'
	data = response.text
	bf = BeautifulSoup(data, 'html.parser')
	root = 'http://www.lr.hainan.gov.cn'
	tb = bf.find_all('table', 'winstyle59832')[0]
	lts = tb.find_all('tr', recursive=False)
	for i in range(0, len(lts)):
		line = lts[i]
		date = line.find_all('td', 'pubtimecontentstyle59832')
		if len(date) != 1:
			continue
		date = date[0].find_all('span')[0].get_text()
		date = datetime.strptime(date, '%Y-%m-%d')
		if date > today or date < lastthreedays:
			continue
		a_tag = line.find_all('td', 'titlecontentstyle59832')[0].find_all('a')[0]
		desp = a_tag.get_text()
		url = root + a_tag.get('href')
		write_to_db(li, desp, url, province, date)
	print province + li[2] + 'done'

def hainan():
	url = [
		[1, 'http://www.lr.hainan.gov.cn/xxgk/list_pt.jsp?urltype=tree.TreeTempUrl&wbtreeid=1358', '政府采购'],
		[3, 'http://www.lr.hainan.gov.cn/xxgk/list_xxgk_2.jsp?urltype=tree.TreeTempUrl&wbtreeid=1367', '公示公告']
	]
	for li in url:
		try:
			hainan_solution(li)
		except Exception as e:
			print e
			continue
		if li != url[-1]:
			time.sleep(7)

def liaoning_solution(li):
	province = '辽宁'
	response = requests.get(li[1])
	response.encoding = 'gb2312'
	data = response.text
	bf = BeautifulSoup(data, 'html.parser')
	root = li[1]
	tb = bf.find_all('div', 'datapage-listshow')[0].find_all('ul')[0]
	lts = tb.find_all('li', recursive=False)
	for i in range(0, len(lts)):
		line = lts[i]
		date = line.find_all('span', 'datetime')
		if len(date) != 1:
			continue
		date = date[0].get_text()
		date = datetime.strptime(date, '%Y-%m-%d')
		if date > today or date < lastthreedays:
			continue
		a_tag = line.find_all('a')[0]
		desp = a_tag.get_text()
		url = root + a_tag.get('href')[2:]
		write_to_db(li, desp, url, province, date)
	print province + li[2] + 'done'

def liaoning():
	url = [
		[2, 'http://www.lgy.gov.cn/gsgg/clps/kyqpgpgbg/', '矿业权评估']
	]
	for li in url:
		try:
			liaoning_solution(li)
		except Exception as e:
			print e
			continue
		if li != url[-1]:
			time.sleep(7)

def chongqing_solution(li):
	province = '重庆'
	response = requests.get(li[1])
	response.encoding = 'GBK'
	data = response.text
	bf = BeautifulSoup(data, 'html.parser')
	root = li[1]
	tb = bf.find_all('ul', 'list')[0]
	lts = tb.find_all('li', recursive=False)
	for i in range(0, len(lts)):
		line = lts[i]
		date = line.find_all('span')
		if len(date) != 1:
			continue
		date = date[0].get_text()
		date = datetime.strptime(date, '%Y-%m-%d')
		if date > today or date < lastthreedays:
			continue
		a_tag = line.find_all('a')[0]
		desp = a_tag.get_text()
		url = root + a_tag.get('href')[2:]
		write_to_db(li, desp, url, province, date)
	print province + li[2] + 'done'

def chongqing():
	url = [
		[1, 'http://www.cqgtfw.gov.cn/gkl/td/', '政府采购']
	]
	for li in url:
		try:
			chongqing_solution(li)
		except Exception as e:
			print e
			continue
		if li != url[-1]:
			time.sleep(7)

def shanxi_solution(li):
	province = '山西'
	response = requests.get(li[1])
	response.encoding = 'gb2312'
	data = response.text
	bf = BeautifulSoup(data, 'html.parser')
	root = 'http://www.shanxilr.gov.cn'
	date_lts = bf.find_all('td', attrs={"class":"listbg", "align":"right"})
	a_lts = bf.find_all('a', 'listA')
	if len(date_lts) != len(a_lts):
		print "山西class长度不匹配"
		return
	for i in range(0, len(a_lts)):
		date = date_lts[i].get_text()
		date = datetime.strptime(date, '%Y-%m-%d')
		if date > today or date < lastthreedays:
			continue
		a_tag = a_lts[i]
		desp = a_tag.get_text()
		url = root + a_tag.get('href')
		write_to_db(li, desp, url, province, date)
	print province + li[2] + 'done'

def shanxi():
	url = [
		[3, 'http://www.shanxilr.gov.cn/Article/ShowClass.asp?ClassID=97', '通知公告']
	]
	for li in url:
		try:
			shanxi_solution(li)
		except Exception as e:
			print e
			continue
		if li != url[-1]:
			time.sleep(7)

def jiangxi_solution(li):
	province = '江西'
	response = requests.get(li[1])
	response.encoding = 'utf-8'
	data = response.text
	bf = BeautifulSoup(data, 'html.parser')
	tb = bf.find_all('table', id='Table')[0]
	lts = bf.find_all('tr')
	root = 'http://www.jxgtt.gov.cn/'
	for i in range(0, len(lts)):
		line = lts[i]
		date = line.find_all('font', attrs={"color":"#a5a4a4"})
		if len(date) != 1:
			continue
		date = date[0].get_text()
		date = datetime.strptime(date, '%Y-%m-%d')
		if date > today or date < lastthreedays:
			continue
		a_tag = line.find_all('a')[0]
		desp = a_tag.get_text()
		url = a_tag.get('href')
		if len(url) > 10 and url[0:11] == 'News.shtml?':
			url = root + url
		write_to_db(li, desp, url, province, date)
	print province + li[2] + 'done'

def jiangxi():
	url = [
		[3, 'http://www.jxgtt.gov.cn/Column.shtml?p5=162', '通知公告']
	]
	for li in url:
		try:
			jiangxi_solution(li)
		except Exception as e:
			print e
			continue
		if li != url[-1]:
			time.sleep(7)

def sichuan_solution(li):
	province = '四川'
	response = requests.get(li[1])
	response.encoding = 'gb2312'
	data = response.text
	bf = BeautifulSoup(data, 'html.parser')
	lts = bf.find_all('div', 'Row')
	root = 'http://www.scdlr.gov.cn'
	for i in range(0, len(lts)):
		line = lts[i]
		date = line.find_all('div', 'Date')[0].get_text()
		date = date.replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
		date = datetime.strptime(date, '%Y-%m-%d')
		if date > today or date < lastthreedays:
			continue
		a_tag = line.find_all('a')[0]
		desp = a_tag.get('title')
		url = root + a_tag.get('href')
		write_to_db(li, desp, url, province, date)
	print province + li[2] + 'done'

def sichuan():
	url = [
		[3, 'http://www.scdlr.gov.cn/sitefiles/services/cms/page.aspx?s=2&n=53', '通知公告']
	]
	for li in url:
		try:
			sichuan_solution(li)
		except Exception as e:
			print e
			continue
		if li != url[-1]:
			time.sleep(7)

def gansu_solution(li):
	province = '甘肃'
	response = requests.get(li[1])
	response.encoding = 'utf-8'
	data = response.text
	bf = BeautifulSoup(data, 'html.parser')
	lts = bf.find_all('li', 'list_txt')
	root = 'http://www.gsdlr.gov.cn:8306/'
	for i in range(0, len(lts)):
		line = lts[i]
		date = line.find_all('span')[0].get_text()
		date = datetime.strptime(date, '%Y-%m-%d')
		if date > today or date < lastthreedays:
			continue
		a_tag = line.find_all('a')[0]
		desp = a_tag.get_text()
		url = root + a_tag.get('href')
		write_to_db(li, desp, url, province, date)
	print province + li[2] + 'done'

def gansu():
	url = [
		[3, 'http://www.gsdlr.gov.cn:8306/list-SUBJ327.htm', '公示公告']
	]
	for li in url:
		try:
			gansu_solution(li)
		except Exception as e:
			print e
			continue
		if li != url[-1]:
			time.sleep(7)
