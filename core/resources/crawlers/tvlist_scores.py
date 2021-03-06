import requests
from bs4 import BeautifulSoup
from utils import browser, save_csv, URL_RESOURCES
from collections import OrderedDict

URL = URL_RESOURCES.get("tv_list_scores")

browser = browser()
browser.get(URL)

content = browser.page_source
parser = BeautifulSoup(content,"html.parser")

data = []

movies = parser.find_all(attrs={"class":"mb-movie"})

for movie in movies:
	
	name = movie.find(attrs={"class":"movieTitle"}).get_text()
	score_item = movie.find(attrs={"class":"tMeterScore"})

	score = score_item.get_text() if score_item else "Sem avaliação"

	movie = OrderedDict()
	movie["nome"] = name
	movie["classificacao"] = score.replace("%","")
	
	data.append(movie)

save_csv(__file__,data)