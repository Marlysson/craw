from selenium import webdriver
from os.path import join, dirname, abspath
import csv

def browser():

	relative_path = dirname(dirname(abspath(__file__)))

	address = join(relative_path,"phantomjs.exe")
	return webdriver.PhantomJS(address)


def save_csv(file=None,data=None):
	if not file:
		raise ValueError("File wasn't found")
	if not data:
		raise ValueError("The 'data' attribute should be filled")

	columns = list(data[0].keys())

	with open(file,"w",newline="") as csv_file:

		csv_writer = csv.DictWriter(csv_file, fieldnames=columns,delimiter=";")
		csv_writer.writeheader()
		csv_writer.writerows(data)

	print("The file {} was wrote successfully.".format(file))
