from bs4 import BeautifulSoup
import requests
from time import sleep
import re
from collections import OrderedDict
from utils import save_csv , URL_RESOURCES

# Separar chamadas de cada página usando asyncio

def get_parsed_content(url):
	content = requests.get(url).content
	parsed_content = BeautifulSoup(content,"html.parser")
	
	return parsed_content

def clean_data(data):
	data = re.sub("[^0-9]","",data)
	data = data.replace(",",".")

	return float(data)

def parsed_data_country(link_country):
	parser = get_parsed_content(URL_BASE + link_country)

	name = parser.find(id="places_country__row").find(class_="w2p_fw").get_text()
	population = parser.find(id="places_population__row").find(class_="w2p_fw").get_text()
	area = parser.find(id="places_area__row").find(class_="w2p_fw").get_text()

	population = clean_data(population)
	area = clean_data(area)

	try:
		density = round(population / area,2)
	except ZeroDivisionError:
		density = 0

	data = OrderedDict()
	data["nome"] = name
	data["populacao"] = population
	data["area"] = area
	data["densidade"] = density

	return data


URL_BASE = URL_RESOURCES.get("countries_infos")
data = []

parser = get_parsed_content(URL_BASE)
next_link = parser.find("a",string="Next >")

while next_link:

	# Collect data
	countries_data = parser.find(id="results")
	countries = countries_data.find_all("td")

	countries_links_from_page = (country.find("a").get("href") for country in countries)

	for country_page in countries_links_from_page:
		data.append(parsed_data_country(country_page))
		sleep(1)

	# Update page with next page...if exists
	next_link = parser.find("a",string="Next >")

	if next_link:
		next_page = URL_BASE + next_link.get("href")
		parser = get_parsed_content(next_page)

save_csv(__file__,data)