from selenium import webdriver
from os import path , getcwd
import csv

CRAWLER_DIR = path.dirname(getcwd())

def browser():

	address = path.join(CRAWLER_DIR,"phantomjs.exe")
	return webdriver.PhantomJS(address)


def save_csv(file=None,data=None):
	if not file:
		raise ValueError("File wasn't found")
	if not data:
		raise ValueError("The 'data' attribute should be filled")

	file_path = path.join(CRAWLER_DIR,"data",file)

	data_columns = list(data[0].keys())

	with open(file_path,"w",newline="") as csv_file:

		csv_writer = csv.DictWriter(csv_file, fieldnames=data_columns,delimiter=";")
		csv_writer.writeheader()
		csv_writer.writerows(data)

	print("The file {} was wrote successfully.".format(file))
