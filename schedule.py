from datetime import datetime, timedelta
from bs4 import BeautifulSoup as Soup
import requests
import re

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
			except BaseException as e:
				print(e)
		return "".join(pair+"\n" for pair in week[datetime.now().weekday()].split("|||")[0:-1])