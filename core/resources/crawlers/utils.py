from selenium import webdriver
import requests
import xml.etree.ElementTree as ET
from os import path , getcwd
import csv

CRAWLER_DIR = path.dirname(getcwd())
DATA_DIR = path.join(CRAWLER_DIR,"data")

URL_RESOURCES = {
    "world_cup": "http://www.portaltransparencia.gov.br/copa2014/api/rest/empreendimento"
}

def browser():

    address = path.join(CRAWLER_DIR,"phantomjs.exe")
    return webdriver.PhantomJS(address)


def save_csv(file=None,data=None):
    if not file:
        raise ValueError("File wasn't found")
    if not data:
        raise ValueError("The 'data' attribute should be filled")

    file_path = path.join(DATA_DIR,file)

    data_columns = list(data[0].keys())

    with open(file_path,"w",newline="") as csv_file:

        csv_writer = csv.DictWriter(csv_file, fieldnames=data_columns,delimiter=";")
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
