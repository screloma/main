import re
from bot_commands import *
import random

def pay_respects(event):
	print(commands)
	try:
		if re.search(commands["футбол_вордфильтр"]["regex"], event.text, re.IGNORECASE) != None:
			return random.choice(["photo191045460_456254363", "photo191045460_456254450"])
	except BaseException as e:
		print(e)
		pass