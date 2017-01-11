# -*- coding:utf-8 -*-

import requests, json, re

class Anchor:
	tv = ''
	room = ''
	is_live = False
	name = None

anchor = Anchor()
anchor.tv = str(input('enter tv:'))
anchor.room = str(input('enter room:'))

class NameGetter:

	def __init__(self, anchor):
		if anchor.tv == u'斗鱼':
			self.douyu(anchor)
		elif anchor.tv == u'熊猫':
			self.xiongmao(anchor)
		elif anchor.tv == u'龙珠':
			self.longzhu(anchor)
		elif anchor.tv == u'全民':
			self.quanmin(anchor)
		elif anchor.tv == u'虎牙':
			self.huya(anchor)
		elif anchor.tv == u'战旗':
			self.zhanqi(anchor)
		else:
			return None

	def douyu(self, anchor):
		try:
			url = 'https://www.douyu.com/' + anchor.room
			r = requests.get(url).text
			pattern = re.compile(r'class="zb-name">(.*?)</a>', re.S)
			anchor.name = re.findall(pattern, r)[0]
		except:
			return None

	def xiongmao(self, anchor):
		try:
			url = 'http://www.panda.tv/' + anchor.room
			r = requests.get(url).text
			pattern = re.compile(r'<title>(.*?)</title>', re.S)
			anchor.name = re.findall(pattern, r)[0][:-16]
		except:
			return None

	def longzhu(self, anchor):
		try:
			url = 'http://star.longzhu.com/' + anchor.room
			r = requests.get(url).text
			pattern = re.compile(r'class="header-info-name">(.*?)</span>', re.S)
			anchor.name = re.findall(pattern, r)[0]
		except:
			return None

	def quanmin(self, anchor):
		try:
			url = 'http://www.quanmin.tv/json/rooms/' + anchor.room + '/noinfo4.json'
			r = requests.get(url).json()
			anchor.name = r.get("nick")
		except:
			return None

	def huya(self, anchor):
		url = 'http://www.huya.com/' + anchor.room
		r = requests.get(url).text
		pattern = re.compile(r' <span class="host-name" title="(.*?)">', re.S)
		anchor.name = re.findall(pattern, r)[0]

	def zhanqi(self, anchor):
		try:
			url = 'https://www.zhanqi.tv/' + anchor.room
			r = requests.get(url).text
			pattern = re.compile(r'<p class="name dv">(.*?)</p>', re.S)
			anchor.name = re.findall(pattern, r)[0]
		except:
			return None

NameGetter(anchor)
print anchor.name
