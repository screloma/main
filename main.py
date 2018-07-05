import argparse 
import sys
from schedule import get_schedule
from bot_auth import *
from solve_integral import *
from respects import *
import re
from bot_commands import *
import http

def start(session, longpoll, cache=""):
	try:
		if cache:
			command = cache["command"]
			event = cache["event"]
			result = eval(command["function"])
			if(not event.from_chat):
				session.method("messages.send", {"user_id" : event.user_id, command["message_type"]: result})
			else:
				session.method("messages.send", {"chat_id" : event.chat_id, command["message_type"]: result})
		for event in longpoll.listen():
			if event.type == VkEventType.MESSAGE_NEW:
				try:
					command = commands[[item 
										for item in commands.keys()
										if re.search(commands[item]["regex"], event.text, re.IGNORECASE) != None]
										[0]]
					print(command)
					cache = {"command": command, "event": event}
					result = eval(command["function"])
					if(not event.from_chat):
						session.method("messages.send", {"user_id" : event.user_id, command["message_type"]: result})
					else:
						session.method("messages.send", {"chat_id" : event.chat_id, command["message_type"]: result})
					cache = ""
				except IndexError as e:
					pass
	except (http.client.RemoteDisconnected, requests.exceptions.ConnectionError, requests.packages.urllib3.exceptions.ProtocolError, TypeError) as e:
		print(e)
		print("Что-то пошло не так, перезагружаемся...")
		start(session, longpoll, cache)
	except BaseException as e:
		print(e)
		print("Что-то пошло не так, перезагружаемся...")
		start(session, longpoll)
			

if __name__ == "__main__":
	try:
		if(len(sys.argv[1]) > 1):
			login = sys.argv[1]
		if(len(sys.argv[2]) > 1):
			passwd = sys.argv[2]
		session, longpoll = authenticate(login, passwd)
		start(session, longpoll)
	except IndexError:
		print("Pass the username and password as arguments.\n")
		exit()





