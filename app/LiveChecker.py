# -*- coding:utf-8 -*-

import requests, json, re

class LiveChecker:

	is_live = False

	def __init__(self, anchor):
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
		url = 'https://www.douyu.com/column_rank_list/getRoomLiveStatusAndCategoryByRoomID?room_id=' + anchor.room
		response = requests.get(url).json()
		is_live = response.get("data").get(anchor.room).get("is_live")
		self.is_live = is_live

	def xiongmao(self, anchor):
		url = 'http://www.panda.tv/' + anchor.room
		r = requests.get(url).text
		pattern = re.compile(r'videoinfo.*?status":"([0-9])",', re.S)
		item = re.findall(pattern, r)
		if item[0] == '2':
			self.is_live = True

	def longzhu(self, anchor):
		url = 'http://star.longzhu.com/' + anchor.room
		api_url = 'http://roomapicdn.plu.cn/room/roomstatus?roomid='
		r1 = requests.get(url).text
		pattern = re.compile(r'"RoomId":(.*?),"Domain"', re.S)
		roomid = re.findall(pattern, r1)[0]
		r2 = requests.get(api_url+str(roomid)).json()
		if r2.get("Broadcast"):
			self.is_live = True

	def quanmin(self, anchor):
		url = 'http://www.quanmin.tv/json/rooms/' + anchor.room + '/noinfo4.json'
		r = requests.get(url).json()
		play_status = r.get("play_status")
		self.is_live = play_status

	def huya(self, anchor):
		url = 'http://www.huya.com/' + anchor.room
		r = requests.get(url).text
		pattern1 = re.compile(r'var REPLAY = (.);', re.S)
		pattern2 = re.compile(r'"isNotLive" : "(.)"', re.S)
		is_replay = re.findall(pattern1, r)
		is_not_live = re.findall(pattern2, r)
		if not is_replay == ['1'] or is_not_live == ['1']:
			self.is_live = True

	def zhanqi(self, anchor):
		url = 'https://www.zhanqi.tv/' + anchor.room
		url_api = 'https://www.zhanqi.tv/api/public/room.liveparam?room_id='
		r1 = requests.get(url).text
		pattern = re.compile(r'<a href="/user/report/room/(.*?)"', re.S)
		roomid = re.findall(pattern, r1)[0]
		r2 = requests.get(url_api+str(roomid)).json()
		if not r2.get("data").get("status") == '0':
			self.is_live = True
