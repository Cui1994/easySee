# -*- coding:utf-8 -*-

import requests, json, re, random
from .logger import namelogger
from ipProtect import USER_AGENTS, PROXIES

class NameGetter:

	s = requests.session()
	s.headers['User-Agent'] = random.choice(USER_AGENTS)
	s.keep_alive = False

	def __init__(self, tv, room):
		self.tv = tv
		self.room = room
		self.name = None
		if self.tv == u'斗鱼':
			self.douyu()
		elif self.tv == u'熊猫':
			self.xiongmao()
		elif self.tv == u'龙珠':
			self.longzhu()
		elif self.tv == u'全民':
			self.quanmin()
		elif self.tv == u'虎牙':
			self.huya()
		elif self.tv == u'战旗':
			self.zhanqi()
		else:
			return None

	def douyu(self):
		try:
			url = 'https://www.douyu.com/' + self.room
			r = self.s.get(url, proxies=random.choice(PROXIES)).text
			pattern = re.compile(r'class="zb-name">(.*?)</a>', re.S)
			self.name = re.findall(pattern, r)[0]
		except:
			namelogger.exception(u'无法连接' + url)
			return None

	def xiongmao(self):
		try:
			url = 'http://www.panda.tv/' + self.room
			r = self.s.get(url, proxies=random.choice(PROXIES)).text
			pattern = re.compile(r'<title>(.*?)</title>', re.S)
			self.name = re.findall(pattern, r)[0][:-16]
		except:
			namelogger.exception(u'无法连接' + url)
			return None

	def longzhu(self):
		try:
			url = 'http://star.longzhu.com/' + self.room
			r = self.s.get(url, proxies=random.choice(PROXIES)).text
			pattern = re.compile(r'class="header-info-name">(.*?)</span>', re.S)
			self.name = re.findall(pattern, r)[0]
		except:
			namelogger.exception(u'无法连接' + url)
			return None

	def quanmin(self):
		try:
			url = 'http://www.quanmin.tv/json/rooms/' + self.room + '/noinfo4.json'
			r = self.s.get(url, proxies=random.choice(PROXIES)).json()
			self.name = r.get("nick")
		except:
			namelogger.exception(u'无法连接' + url)
			return None

	def huya(self):
		try:
			url = 'http://www.huya.com/' + self.room
			r = self.s.get(url, proxies=random.choice(PROXIES)).text
			pattern = re.compile(r' <span class="host-name" title="(.*?)">', re.S)
			self.name = re.findall(pattern, r)[0]
		except:
			namelogger.exception(u'无法连接' + url)
			return None

	def zhanqi(self):
		try:
			url = 'https://www.zhanqi.tv/' + self.room
			r = self.s.get(url, proxies=random.choice(PROXIES)).text
			pattern = re.compile(r'<p class="name dv">(.*?)</p>', re.S)
			self.name = re.findall(pattern, r)[0]
		except:
			namelogger.exception(u'无法连接' + url)
			return None
