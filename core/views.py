from django.shortcuts import render
from .utils import load_formatted, generate_colors

def view_world_cup_expenses(request):

	content = load_formatted("spent_world_cup.csv")

	labels = [line["nome"] for line in content]
	values = [float(line["valor"].strip()) for line in content]

	background_color, border_color = generate_colors(len(labels),alpha=0.2)

	context = {
		"labels": labels,
		"values": values,
		"background_color": background_color,
		"border_color": border_color
	}

	return render(request,"world-cup.html",context)


def series_review(request):

	# content = open(settings.BASE_DIR+"/core/data/series_infos.csv").readlines()

	head = content[0]
	content = content[1:]

	labels = [value.split(";")[0] for value in content]
	reviews = [value.split(";")[1].replace("%","").strip() for value in content]

	data_value = []

	cont_without_review = 0

	for value in reviews:
		if value == 'Sem avaliação':
			data_value.append(0)
			cont_without_review += 1
		else:
			data_value.append(float(value.replace("%","")))


	all_colors = []

	for _ in range(len(labels)):
		colors = sample(range(0,256),3)
		colors = ",".join(list(map(str,colors)))
		colors = "rgb({})".format(colors)
		all_colors.append(colors)

	context = {
		"labels":labels,
		"values":data_value,
		"colors":all_colors,
		"pie_chart":[cont_without_review, len(data_value) - cont_without_review],
		"pie_labels":["Com revisões","Sem revisões"]
	}

	return render(request,"review_series.html",context)