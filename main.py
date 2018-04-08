from vk_api import *
from vk_api.longpoll import *
import requests
from bs4 import BeautifulSoup as Soup
from datetime import *
import random
import sys
from sympy import integrate, erf, exp, sin, log, oo, pi, sinh, symbols, preview, Integral
from sympy.abc import x
from mpmath import *
import re
from sympy.parsing.sympy_parser import parse_expr
import base64
import json
import http
import itertools


imgur_token = "9c2f88fb8600dbbc047fb02c5c9a2547c230a193"
vk = VkApi(login="79517688763", password="bloodshot1A")
vk.auth()
longpoll = VkLongPoll(vk)
cache = ""

def get_schedule():
	weekstart = (datetime.now()-timedelta(days=datetime.now().weekday()))
	weekend = (datetime.now()+timedelta(days=6-datetime.now().weekday()))
	if(datetime.now().weekday() == 6):
		print("Сегодня пар нет!")
		return "Сегодня пар нет!"
	else:
		weekrange = "{0:0>2}".format(str(weekstart.day))+str('%02d' % weekstart.month)+str(weekstart.year)+"{0:0>2}".format(str(weekend.day))+str('%02d' % weekend.month)+str(weekend.year)
		params={"group": "07001701", "week": weekrange}
		page = Soup(requests.get("https://www.bsu.edu.ru/bsu/resource/schedule/groups/show_schedule.php", params=params).text, "lxml")
		with open("/mnt/g/dev/bot/bstu.html", "w") as file:
			file.write(str(page))
		days = [day for day in page.find_all('table')[1].find_all("tr")]
		week = [day.text+"\r\n" for day in page.find_all('table')[1].select(".h3")]
		print(weekrange)
		i=0
		for day in days:
			try:
				children = len(list(day.find_all("td")))
				if children > 3:
					for pair in day.find_all("td"):
						week[i-1]+=str(" " + re.sub(r" +", " ", pair.text.strip().replace("\n", ' ')) + " ")
					week[i-1]+="|||"
				else:
					i+=1
			except e:
				print(e)
		return "".join(pair+"\n" for pair in week[datetime.now().weekday()].split("|||")[0:-1])

def solve_integral(event):
	print(event.text.split("неопределённый интеграл")[1])
	preview(integrate(parse_expr(event.text.split("неопределённый интеграл")[1])), viewer="file", filename="/mnt/g/dev/answer.png")
	encoded = ""
	url = vk.method("photos.getMessagesUploadServer", {"peer_id": event.user_id})
	print(url["upload_url"])
	photo = requests.post(url["upload_url"], files = {"photo": open("/mnt/g/dev/answer.png", "rb")}).json()
	uploaded = vk.method("photos.saveMessagesPhoto", {"photo" : photo["photo"], "server": photo["server"],"hash": photo["hash"]})
	print(uploaded[0])
	print(str(uploaded[0]["owner_id"])+"_"+str(uploaded[0]["id"]))
	return "photo"+str(uploaded[0]["owner_id"])+"_"+str(uploaded[0]["id"])
	print(get_schedule())
	print(sys.version)

def listen_(event, cache=""):
	if event.type == VkEventType.MESSAGE_NEW:
			try:
				if (not event.from_chat):
					if(re.search("неопределённый интеграл", event.text, re.IGNORECASE)):
						vk.method("messages.send", {"user_id" : event.user_id, "attachment": solve_integral(event)})
					if(re.search("д[н]?[оo]{1}т[каaoоуyыеeи]{1}", event.text, re.IGNORECASE)):
						vk.method('messages.send', {'user_id': event.user_id, 'message': "нахуй с конфы вышел"})
					if(re.search("где пара\??", event.text, re.IGNORECASE)):
						vk.method('messages.send', {'user_id': event.user_id, 'message': get_schedule()})
				else:
					if(re.search("неопределённый интеграл", event.text, re.IGNORECASE)):
						vk.method("messages.send", {"chat_id" : event.chat_id, "attachment": solve_integral(event)})
					if(re.search("где пара\??", event.text, re.IGNORECASE)):
						vk.method('messages.send', {'chat_id': event.chat_id, 'message': get_schedule()})
					if(re.search("д[н]?[оo]{1}т[каaoоуyыеeи]{1}", event.text, re.IGNORECASE)):
						vk.method('messages.send', {'chat_id': event.chat_id, 'message': "нахуй с конфы вышел"})
				if not event.to_me:
					if(re.search("ролл", event.text, re.IGNORECASE)):
						user = vk.method("users.get", {"user_ids": event.user_id})[0]
						for user in chat_users:
							object_ = vk.method("users.get", {"user_ids": user})[0]
							users.append(object_["first_name"]+" "+object_["last_name"])
						print(users)
						print(random.sample(users, 10))
						if(event.from_chat):
							vk.method('messages.send', {'chat_id': event.chat_id, 'message': "На олимпиаду идут: " + str(random.sample(users, 2))})
			except (http.client.RemoteDisconnected, requests.exceptions.ConnectionError, requests.packages.urllib3.exceptions.ProtocolError) as e:
				print(str(e))
				cache = event
				print(cache.text)
				print("Reconnecting...")
				startPolling(cache)

def startPolling(cache):
	print("Started polling...")
	longpoll = VkLongPoll(vk)
	chat = 121
	if(cache):
		listen_(cache)
	for event in longpoll.listen():
		listen_(event)
if __name__ == "__main__":
	startPolling(cache)
		
