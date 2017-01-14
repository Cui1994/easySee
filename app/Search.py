# -*- coding:utf-8 -*-

import requests, json, re, random
from .logger import searchlogger
from ipProtect import USER_AGENTS, PROXIES

class AnchorSearch:
	name = ''
	tv = ''
	room = ''
	url = ''

class Search:

	requests.adapters.DEFAULT_RETRIES = 5
	s = requests.session()
	s.headers['User-Agent'] = random.choice(USER_AGENTS)
	s.keep_alive = False

	def __init__(self, query):
		self.anchors = []
		self.query = query
		self.search_douyu()
		self.search_xiongmao()
		self.search_longzhu()
		self.search_zhanqi()

	def search_douyu(self):
		try:
			resc = []
			url = 'https://www.douyu.com/search?kw=' + self.query
			r = self.s.get(url, proxies=random.choice(PROXIES)).text
			pattern1 = re.compile(r'<ul class="anchor-list-box">(.*?)<div  class="video-list t-video" id="search-room-list">', re.S)
			list_text = re.findall(pattern1, r)[0]
			pattern2 = re.compile(r'<a href="/(.*?)" data-rid=.*?<h3>(.*?)</h3>', re.S)
			items = re.findall(pattern2, list_text)
			pattern3 = re.compile(r'<.*?>', re.S)
			if items != []:
				for item in items:
					anchor = AnchorSearch()
					anchor.name = pattern3.sub('', item[1])
					anchor.room = item[0]
					anchor.tv = u'斗鱼'
					anchor.url = 'https://www.douyu.com/' + anchor.room
					resc.append(anchor)
			if len(resc)>2:
				resc = resc[:2]
			self.anchors += resc
		except:
			searchlogger.exception(u'无法连接' + url)

	def search_xiongmao(self):
		try:
			resc = []
			url = 'http://www.panda.tv/ajax_search?nickname='+self.query+'&order_cond=fans'
			r = self.s.get(url, proxies=random.choice(PROXIES)).json()
			items = r.get("data").get("items")
			pattern = re.compile(r'<.*?>', re.S)
			if items != []:
				for item in items:
					anchor = AnchorSearch()
					anchor.name = pattern.sub('', item.get("nickname"))
					anchor.tv = u'熊猫'
					anchor.room = item.get("roomid")
					anchor.url = 'http://www.panda.tv/' + anchor.room
					resc.append(anchor)
			if len(resc)>2:
				resc = resc[:2]
			self.anchors += resc
		except:
			searchlogger.exception(u'无法连接' + url)

	def search_longzhu(self):
		try:
			resc = []
			url = 'http://searchapi.plu.cn/api/search/room?title=' + self.query
			r = self.s.get(url, proxies=random.choice(PROXIES)).json()
			items = r.get("items")
			if items != []:
				anchor = AnchorSearch()
				anchor.name = items[0].get("name")
				anchor.room = items[0].get("domain")
				anchor.tv = u'龙珠'
				anchor.url = 'http://star.longzhu.com/' + anchor.room
				resc.append(anchor)
			self.anchors += resc
		except:
			searchlogger.exception(u'无法连接' + url)

	def search_zhanqi(self):
		try:
			resc = []
			url = 'https://www.zhanqi.tv/search?t=anchor&q=' + self.query
			r = self.s.get(url, proxies=random.choice(PROXIES)).text
			pattern1 = re.compile(r'<div class="left-anchor.*?<a href="/(.*?)" class="img-box">.*?<p class="name dv"><em>(.*?)</em></p>', re.S)
			items = re.findall(pattern1, r)
			pattern2 = re.compile(r'<.*?>', re.S)
			if items != []:
				for item in items:
					anchor = AnchorSearch()
					anchor.name = pattern2.sub('', item[1])
					anchor.room = item[0]
					anchor.tv = u'战旗'
					anchor.url = 'https://www.zhanqi.tv/' + anchor.room
					resc.append(anchor)
			if len(resc)>2:
				resc = resc[:2]
			self.anchors += resc
		except:
			searchlogger.exception(u'无法连接' + url)
