from vk_api import *
from sympy import integrate, erf, exp, sin, log, oo, pi, sinh, symbols, preview, Integral
from sympy.abc import x
from mpmath import *
from sympy.parsing.sympy_parser import parse_expr
from bot_commands import *
import re

def solve_integral(event, session):
	print(event.text)
	integral = event.text.replace(re.search(commands["неопределённый интеграл"]["regex"], event.text, re.IGNORECASE).group(0), '').strip()
	preview(integrate(parse_expr(integral)), viewer="file", filename="answer.png")
	upload = VkUpload(session)
	photo = upload.photo_messages(
		"answer.png"
		)
	print(photo)
	return f'photo{str(photo[0]["owner_id"])}_{str(photo[0]["id"])}'