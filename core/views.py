from django.shortcuts import render
from .utils import load_formatted, generate_colors
from random import sample

def tv_series_review(request):

	content = load_formatted("tvlist_scores.csv")
	series_without_review = []

	labels = []
	values = []
	pie_colors = []

	for item in content:
		if item["classificacao"] != "Sem avaliação":
			labels.append(item["nome"])
			values.append(item["classificacao"])
		else:
			series_without_review.append(item["nome"])

	background_color, border_color = generate_colors(len(labels),alpha=0.5)

	for _ in range(2):
		pie_background = sample(range(0,256),3)
		pie_background = "rgb({})".format(",".join(list(map(str, pie_background))))
		pie_colors.append(pie_background)

	context = {
		"labels":labels,
		"values":values,
		"background": background_color,
		"border": border_color,
		"pie_chart_values": [len(content) - len(series_without_review) , len(series_without_review)],
		"pie_colors": pie_colors,
		"series_without_review":series_without_review
	}

	return render(request,"review_series.html",context)

def view_world_cup_expenses(request):

	content = load_formatted("world_cup_expenses.csv")

	labels = [line["uf"] for line in content]
	values = [float(line["negociado"].strip()) for line in content]

	background_color, border_color = generate_colors(len(labels),alpha=0.2)
	
	context = {
		"labels": labels,
		"values": values,
		"background_color": background_color,
		"border_color": border_color
	}

	return render(request,"world-cup.html",context)


