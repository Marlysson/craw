from bs4 import BeautifulSoup
import requests
from utils import save_csv, save_file_as , URL_RESOURCES
from collections import OrderedDict

URL = URL_RESOURCES.get("films_money")
content = requests.get(URL).content

parser = BeautifulSoup(content,"html.parser")

table = parser.find("table",attrs={"data-caller-name":"chart-boxoffice"})
content_table = table.find("tbody")

data = []

for film_info in content_table.find_all("tr"):

	name = film_info.find("td",class_="titleColumn").find("a").get_text()
	bill_weekend = film_info.find("td",class_="ratingColumn").get_text().replace("$","")

	if bill_weekend.strip()[-1] == "M":
		bill_weekend = float(bill_weekend.replace("M",""))
		bill_weekend *= 1000000

	gross_value = film_info.find("span",class_="secondaryInfo").get_text().replace("$","")

	if gross_value.strip()[-1] == "M":
		gross_value = float(gross_value.replace("M",""))
		gross_value *= 1000000

	week_rank = film_info.find("td",class_="weeksColumn").get_text()

	item = OrderedDict()
	item["nome"] = name.strip()
	item["valor_semanal"] = bill_weekend
	item["valor_acumulado"] = gross_value
	item["quantidade_semanas"] = week_rank.strip()

	data.append(item)

save_csv(__file__,data=data)