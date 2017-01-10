# -*- coding:utf-8 -*-

import requests, json, re

class Anchor:
	tv = ''
	room = ''
	is_live = False

anchor = Anchor()
anchor.tv = str(input('enter tv:'))
anchor.room = str(input('enter room:'))

class LiveChecker:

	def __init__(self, anchor):
		if anchor.tv == 'douyu':
			self.douyu(anchor)
		elif anchor.tv == 'xiongmao':
			self.xiongmao(anchor)
		elif anchor.tv == 'longzhu':
			self.longzhu(anchor)
		elif anchor.tv == 'quanmin':
			self.quanmin(anchor)
		elif anchor.tv == 'huya':
			self.huya(anchor)
		elif anchor.tv == 'zhanqi':
			self.zhanqi(anchor)
		else:
			return None

	def douyu(self, anchor):
		url = 'https://www.douyu.com/column_rank_list/getRoomLiveStatusAndCategoryByRoomID?room_id=' + anchor.room
		response = requests.get(url).json()
		is_live = response.get("data").get(anchor.room).get("is_live")
		anchor.is_live = is_live

	def xiongmao(self, anchor):
		url = 'http://www.panda.tv/' + anchor.room
		r = requests.get(url).text
		pattern = re.compile(r'videoinfo.*?status":"([0-9])",', re.S)
		item = re.findall(pattern, r)
		if item[0] == '2':
			anchor.is_live = True

	def longzhu(self, anchor):
		url = 'http://star.longzhu.com/' + anchor.room
		api_url = 'http://roomapicdn.plu.cn/room/roomstatus?roomid='
		r1 = requests.get(url).text
		pattern = re.compile(r'"RoomId":(.*?),"Domain"', re.S)
		roomid = re.findall(pattern, r1)[0]
		r2 = requests.get(api_url+str(roomid)).json()
		if r2.get("Broadcast"):
			anchor.is_live = True

	def quanmin(self, anchor):
		url = 'http://www.quanmin.tv/json/rooms/' + anchor.room + '/noinfo4.json'
		r = requests.get(url).json()
		play_status = r.get("play_status")
		anchor.is_live = play_status

	def huya(self, anchor):
		url = 'http://www.huya.com/' + anchor.room
		r = requests.get(url).text
		pattern1 = re.compile(r'var REPLAY = (.);', re.S)
		pattern2 = re.compile(r'"isNotLive" : "(.)"', re.S)
		is_replay = re.findall(pattern1, r)
		is_not_live = re.findall(pattern2, r)
		if not is_replay == ['1'] or is_not_live == ['1']:
			anchor.is_live = True

	def zhanqi(self, anchor):
		url = 'https://www.zhanqi.tv/' + anchor.room
		url_api = 'https://www.zhanqi.tv/api/public/room.liveparam?room_id='
		r1 = requests.get(url).text
		pattern = re.compile(r'<a href="/user/report/room/(.*?)"', re.S)
		roomid = re.findall(pattern, r1)[0]
		r2 = requests.get(url_api+str(roomid)).json()
		if not r2.get("data").get("status") == '0':
			anchor.is_live = True

LiveChecker(anchor)
if anchor.is_live:
	print 'the room is living'
else:
	print 'the room is closed'