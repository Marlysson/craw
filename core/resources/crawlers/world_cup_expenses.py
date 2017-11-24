import xml.etree.ElementTree as ET
from collections import OrderedDict
import os
import requests
from utils import save_csv
from bs4 import BeautifulSoup

URL = "http://www.portaltransparencia.gov.br/copa2014/api/rest/empreendimento"

file_name = "world_cup_expense.xml"

def is_valid_file():
	if os.path.exists(file_name):
		if os.path.getsize(file_name) > 0:
			return True
		return False
	return False
		 

if not is_valid_file():
	with open(file_name,"w") as xml:
		content = requests.get(URL).text
		xml.write(content)

with open(file_name) as xml:
	root = ET.fromstring(xml.read())

data = {}

for spent in root:

	try:
		value = spent.find("valorTotalPrevisto").text
		uf = spent.find("uf").find("nome").text
		if uf in data:
			data[uf] += float(value)
		else:
			data[uf] = float(value)
	except:
		pass

def total_spent():
	return sum(data.values())

formatted = [OrderedDict([("nome",nome),("valor",round(valor,2))]) for nome,valor in data.items()]
print("Total gasto: {:,.2f}".format(total_spent()))

for data in formatted:
	data = dict(data)
	print("{}:{:,.2f}".format(data["nome"],data["valor"]))

save_csv("spent_world_cup.csv",data=formatted)
