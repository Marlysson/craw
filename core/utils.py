import os
from django.conf import settings
from django.apps import apps
from random import sample
import csv

def full_path(file_name):
	
	current_app = apps.get_app_config("core")
	DATA_PATH = os.path.join(current_app.path,"resources","data")

	file_path = os.path.join(DATA_PATH,file_name)
	return file_path


def load_formatted(file_name):

	file_name = full_path(file_name)

	with open(file_name,newline='') as csv_file:
		file_content = csv.DictReader(csv_file,delimiter=",")
		return [dict(line) for line in file_content]

def generate_colors(count=None,alpha=0.5,different=False):

	if different:
		colors = []

		for _ in range(count):
			background = sample(range(0,256),3)
			
			background = ",".join(list(map(str, background + [alpha] )))
			background = "rgba({})".format(background)			
			colors.append(background)

		return colors

	else:
		background_color = sample(range(0,256),3)
		border_color = background_color + [1]

		background_color = ",".join(list(map(str, background_color + [alpha] )))
		background_color = "rgba({})".format(background_color)

		border_color = ",".join(list(map(str,border_color)))
		border_color = "rgba({})".format(border_color)

		background_color = [background_color] * count
		border_color = [border_color] * count

		return background_color , border_color

def sort_it(type_python,value_to_order=None):

	if isinstance(type_python,dict):
		return sorted(type_python.items(),key=lambda x : x[1], reverse=True)
	elif isinstance(type_python,list):
		return (sorted(type_python,key=lambda x : float(x[value_to_order]),reverse=True))
