import argparse 
from vk_api import *
from vk_api.longpoll import *
from io import BytesIO
from PIL import Image
import requests

def two_factor_handler():
    code = input('Code? ')
    return code, True

def captcha_handler(captcha):
	print(captcha.get_url())
	response = requests.get(captcha.get_url(), stream=True)
	img = Image.open(BytesIO(response.raw.read()))
	img.show()
	return captcha.try_again(input("Введите код с картинки: "))

def authenticate(login, passwd):
	session = VkApi(login=login,
			password=passwd,
			auth_handler=two_factor_handler,
			captcha_handler=captcha_handler)
	session.auth()
	longpoll = VkLongPoll(session)
	return session, longpoll
