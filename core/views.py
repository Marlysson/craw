from django.shortcuts import render
from .utils import load_formatted, generate_colors
from random import sample
from collections import defaultdict

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

def films_money(request):

	content = load_formatted("films_money.csv")
	
	labels, values_weekend, values_total,weeks_ranking = [], [], [], []

	for item in content:
		labels.append(item["nome"])
		values_weekend.append(float(item["valor_semanal"]))
		values_total.append(float(item["valor_acumulado"]))
		weeks_ranking.append(int(item["quantidade_semanas"]))

	background_color_one , color_border_one = generate_colors(len(labels),alpha=0.5)
	background_color_two , color_border_two = generate_colors(len(labels),alpha=0.5)
	background_three = generate_colors(len(labels),different=True)

	context = {
		"labels":labels,
		"values_weekend":values_weekend,
		"values_total":values_total,
		"weeks_ranking":weeks_ranking,
		"background_one": background_color_one,
		"border_one":color_border_one,
		"background_two":background_color_two,
		"border_two":color_border_two,
		"background_three":background_three
	}

	return render(request,"films-money.html",context)

def view_world_cup_expenses(request):

	content = load_formatted("world_cup_expenses.csv")

	spent_countries = {}

	# Gasto por Estado

	for spent in content:
		if spent["uf"] in spent_countries:
			spent_countries[spent["uf"]] += float(spent["negociado"])
		else:
			spent_countries[spent["uf"]] = 0.0
		
	background , border = generate_colors(len(list(spent_countries)))
	
	labels, values = [] , []	

	for item in spent_countries:
		labels.append(item)
		values.append(spent_countries[item])

	# Gasto por tipo de infraestrutura

	types_construction = defaultdict(float)

	for item in content:
		types_construction[item["tema"]] += float(item["negociado"])

	colors_pie = generate_colors(len(types_construction),different=True)

	# Gasto por Instituição efetivamente construtora

	institution = defaultdict(float)

	for spent in content:
		institution[spent["instituicao"]] += float(spent["negociado"])

	ordered_instituition_spent = sorted(institution.items(),key=lambda x : x[1], reverse=True)

	institution_labels , institution_values = [] , []

	for institution,value in ordered_instituition_spent:
		institution_labels.append(institution)
		institution_values.append(value)

	background_institution , border_institution = generate_colors(len(ordered_instituition_spent))

	context = {
		"label_countries" : labels,
		"values_negotiated" : values,
		"background": background,
		"border": border,

		"total_spent": "{:,.2f}".format(sum(values)),
	
		"labels_type_construction": list(types_construction.keys()),
		"values_type_construction": list(types_construction.values()),
		
		"color_pie" : colors_pie,

		"institution_label" : institution_labels,
		"institution_values": institution_values,
		
		"background_institution" : background_institution,
		"border_institution": border_institution
	}

	return render(request,"world-cup.html",context)