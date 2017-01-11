# -*- coding:utf-8 -*-

import requests, json, re

class NameGetter:

	def __init__(self, tv, room):
		self.tv = tv
		self.room = room
		self.name = None
		if self.tv == 'douyu':
			self.douyu()
		elif self.tv == 'xiongmao':
			self.xiongmao()
		elif self.tv == 'longzhu':
			self.longzhu()
		elif self.tv == 'quanmin':
			self.quanmin()
		elif self.tv == 'huya':
			self.huya()
		elif self.tv == 'zhanqi':
			self.zhanqi()
		else:
			return None

	def douyu(self):
		try:
			url = 'https://www.douyu.com/' + self.room
			r = requests.get(url).text
			pattern = re.compile(r'class="zb-name">(.*?)</a>', re.S)
			self.name = re.findall(pattern, r)[0]
		except:
			return None

	def xiongmao(self):
		try:
			url = 'http://www.panda.tv/' + self.room
			r = requests.get(url).text
			pattern = re.compile(r'<title>(.*?)</title>', re.S)
			self.name = re.findall(pattern, r)[0][:-16]
		except:
			return None

	def longzhu(self):
		try:
			url = 'http://star.longzhu.com/' + self.room
			r = requests.get(url).text
			pattern = re.compile(r'class="header-info-name">(.*?)</span>', re.S)
			self.name = re.findall(pattern, r)[0]
		except:
			return None

	def quanmin(self):
		try:
			url = 'http://www.quanmin.tv/json/rooms/' + self.room + '/noinfo4.json'
			r = requests.get(url).json()
			self.name = r.get("nick")
		except:
			return None

	def huya(self):
		url = 'http://www.huya.com/' + self.room
		r = requests.get(url).text
		pattern = re.compile(r' <span class="host-name" title="(.*?)">', re.S)
		self.name = re.findall(pattern, r)[0]

	def zhanqi(self):
		try:
			url = 'https://www.zhanqi.tv/' + self.room
			r = requests.get(url).text
			pattern = re.compile(r'<p class="name dv">(.*?)</p>', re.S)
			self.name = re.findall(pattern, r)[0]
		except:
			return None
