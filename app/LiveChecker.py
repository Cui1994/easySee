# -*- coding:utf-8 -*-

import requests, json, re, random
from .logger import livelogger
from ipProtect import USER_AGENTS, PROXIES

class LiveChecker:

	is_live = False
	s = requests.session()
	s.headers['User-Agent'] = random.choice(USER_AGENTS)

	def __init__(self, anchor):
		self.is_live = anchor.is_live
		if anchor.tv.name == u'斗鱼':
			self.douyu(anchor)
		elif anchor.tv.name == u'熊猫':
			self.xiongmao(anchor)
		elif anchor.tv.name == u'龙珠':
			self.longzhu(anchor)
		elif anchor.tv.name == u'全民':
			self.quanmin(anchor)
		elif anchor.tv.name == u'虎牙':
			self.huya(anchor)
		elif anchor.tv.name == u'战旗':
			self.zhanqi(anchor)

	def douyu(self, anchor):
		try:
			room_id = anchor.room
			if not room_id.isdigit():
				url = 'https://www.douyu.com/'+ room_id
				r = self.s.get(url).text
				pattern = re.compile(r'ROOM = {"room_id":(.*?),', re.S)
				room_id = re.findall(pattern, r)[0]
			url = 'https://www.douyu.com/column_rank_list/getRoomLiveStatusAndCategoryByRoomID?room_id=' + room_id
			response = self.s.get(url, proxies=random.choice(PROXIES)).json()
			is_live = response.get("data").get(room_id).get("is_live")
			self.is_live = is_live
		except:
			livelogger.exception(u'无法连接' + url)

	def xiongmao(self, anchor):
		try:
			url = 'http://www.panda.tv/' + anchor.room
			r = self.s.get(url, proxies=random.choice(PROXIES)).text
			pattern = re.compile(r'videoinfo.*?status":"([0-9])",', re.S)
			item = re.findall(pattern, r)
			if item[0] == '2':
				self.is_live = True
		except:
			livelogger.exception(u'无法连接' + url)

	def longzhu(self, anchor):
		try:
			url = 'http://star.longzhu.com/' + anchor.room
			api_url = 'http://roomapicdn.plu.cn/room/roomstatus?roomid='
			r1 = self.s.get(url, proxies=random.choice(PROXIES)).text
			pattern = re.compile(r'"RoomId":(.*?),"Domain"', re.S)
			roomid = re.findall(pattern, r1)[0]
			r2 = self.s.get(api_url+str(roomid), proxies=random.choice(PROXIES)).json()
			if r2.get("Broadcast"):
				self.is_live = True
		except:
			livelogger.exception(u'无法连接' + url)

	def quanmin(self, anchor):
		try:
			url = 'http://www.quanmin.tv/json/rooms/' + anchor.room + '/noinfo4.json'
			r = self.s.get(url, proxies=random.choice(PROXIES)).json()
			play_status = r.get("play_status")
			self.is_live = play_status
		except:
			livelogger.exception(u'无法连接' + url)

	def huya(self, anchor):
		try:
			url = 'http://www.huya.com/' + anchor.room
			r = self.s.get(url, proxies=random.choice(PROXIES)).text
			pattern1 = re.compile(r'var REPLAY = (.);', re.S)
			pattern2 = re.compile(r'"isNotLive" : "(.)"', re.S)
			is_replay = re.findall(pattern1, r)
			is_not_live = re.findall(pattern2, r)
			if not (is_replay == ['1'] or is_not_live == ['1']):
				self.is_live = True
		except:
			livelogger.exception(u'无法连接' + url)

	def zhanqi(self, anchor):
		try:
			url = 'https://www.zhanqi.tv/' + anchor.room
			url_api = 'https://www.zhanqi.tv/api/public/room.liveparam?room_id='
			r1 = self.s.get(url, proxies=random.choice(PROXIES)).text
			pattern = re.compile(r'<a href="/user/report/room/(.*?)"', re.S)
			roomid = re.findall(pattern, r1)[0]
			r2 = self.s.get(url_api+str(roomid), proxies=random.choice(PROXIES)).json()
			if not r2.get("data").get("status") == '0':
				self.is_live = True
		except:
			livelogger.exception(u'无法连接' + url)
