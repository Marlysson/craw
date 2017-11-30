import requests
from bs4 import BeautifulSoup

from datetime import datetime
import time
from collections import OrderedDict

from utils import load_formatted, save_csv, browser, URL_RESOURCES
import re

import schedule

# Capture all time , verify the length of content already saved.
# If bigger than 5 , remove the last and insert the new data.

# def job():

all_mensures = load_formatted("clima_tempo.csv")

def get_time(text):
	return re.search(r"\d{2}:\d{2}",text).group(0).split(":")

def crawler_page():
	b = browser()
	b.get(URL_RESOURCES.get("clima_tempo"))

	content = b.page_source
	b.close()

	content_parsed = BeautifulSoup(content,"html.parser")
	return content_parsed

def is_new(new_mensure):
	if not all_mensures:
		return True

	last_mensure = all_mensures[-1]

	old_datetime = datetime.strptime(last_mensure["time"],"%Y/%m/%d %H:%M:%S")

	if new_mensure >= old_datetime:
		return True
	return False


content = crawler_page()

today = datetime.today()

update_at = content.find(id="momento-atualizacao").get_text()
print(update_at)
update_at = get_time(update_at)

hour,minutes = int(update_at[0]), int(update_at[1])

now = today.replace(microsecond=0)
now = now.replace(hour=hour,minute=minutes)

temperature = content.find(id="momento-temperatura").get_text().replace("°","")

if is_new(now):
	if len(all_mensures) == 5:
		all_mensures.remove(0)

	now = datetime.strftime(now,"%d/%m/%Y %I:%M:%S")
	
	data = OrderedDict()
	data["temperature"] = temperature
	data["time"] = now
	
	all_mensures.append(data)

	save_csv(__file__, all_mensures)

# schedule.every(1).second.do(job)

# while True:
# 	schedule.run_pending()
# 	time.sleep(1)