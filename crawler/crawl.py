#coding=utf-8

import functions

lists = [
	'guangdong',
	'anhui',
	'hunan',
	'yunnan',
	'shandong',
	'jiangsu',
	'guangxi',
	'henan',
	'guizhou',
	'ningxia',
	'liaoning',
	'chongqing',
	'shanxi',
	'jiangxi',
	'sichuan',
	'gansu'
]

for i in range(0, len(lists)):
	eval('functions.' + lists[i] + '()')
