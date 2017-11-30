from selenium import webdriver
import requests
import xml.etree.ElementTree as ET
from os import path , getcwd
import csv
from datetime import datetime

CRAWLER_DIR = path.dirname(getcwd())
DATA_DIR = path.join(CRAWLER_DIR,"data")

URL_RESOURCES = {
    "world_cup": "http://www.portaltransparencia.gov.br/copa2014/api/rest/empreendimento",
    "countries_infos": "http://example.webscraping.com",
    "films_money": "http://www.imdb.com/chart/boxoffice",
    "tv_list_scores": "https://www.rottentomatoes.com/browse/tv-list-1",
    "clima_tempo" : "https://www.climatempo.com.br/previsao-do-tempo/cidade/264/teresina-pi"
}

def save_file_as(scope):
    filename = scope.split(".")[0] + ".csv"
    return filename

def browser():

    address = path.join(CRAWLER_DIR,"phantomjs.exe")
    return webdriver.PhantomJS(address)

def save_csv(file=None,data=None):
    if not file:
        raise ValueError("File wasn't found")
    if not data:
        raise ValueError("The 'data' attribute should be filled")

    file = save_file_as(file)

    file_path = path.join(DATA_DIR,file)

    data_columns = list(data[0].keys())

    with open(file_path,"w",newline="") as csv_file:

        csv_writer = csv.DictWriter(csv_file, fieldnames=data_columns,delimiter=",")
        csv_writer.writeheader()
        csv_writer.writerows(data)

    print("The file {} was wrote successfully.".format(file))


def load_xml_resource(filename):

    file_path = path.join(DATA_DIR,filename)
    
    if not path.exists(file_path):
        with open(file_path,"w") as xml:

            url = URL_RESOURCES.get("world_cup")
            
            content = requests.get(url).text
            xml.write(content)          
    
    with open(file_path) as xml:
        root = ET.fromstring(xml.read())
    return root

def load_formatted(file_name):

    file_name = path.join(DATA_DIR,file_name)

    if path.exists(file_name):

        with open(file_name,newline='') as csv_file:
            file_content = csv.DictReader(csv_file,delimiter=",")

            formatted = []

            content = [dict(line) for line in file_content]

            for item in content:
                formatted.append({"time":item["time"],"temperature":item["temperature"]})

            return formatted
    else:
        return []
