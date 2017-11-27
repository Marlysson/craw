from django.shortcuts import render
from .utils import load_formatted, generate_colors , sort_it
from random import sample
from collections import defaultdict

def tv_series_review(request):

	content = load_formatted("tvlist_scores.csv")
	series_without_review = []

	labels = []
	values = []
	pie_colors = []

	data_tv_series = {}

	for item in content:
		if item["classificacao"] != "Sem avaliação":
			data_tv_series[item["nome"]] = float(item["classificacao"].replace("%",""))
		else:
			series_without_review.append(item["nome"])

	data_tv_series = sort_it(data_tv_series)

	for item,value in data_tv_series:
		labels.append(item)
		values.append(value)

	background_color, border_color = generate_colors(len(data_tv_series))

	pie_colors = generate_colors(len(labels),different=True)

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

	spent_countries = defaultdict(float)

	for spent in content:
		spent_countries[spent["uf"]] += float(spent["negociado"])
	
	spent_countries = sort_it(spent_countries)

	background , border = generate_colors(len(list(spent_countries)))
	
	labels, values = [] , []	

	for item,value in spent_countries:
		labels.append(item)
		values.append(value)

	# Gasto por tipo de construção ( Aeroporto , Mobilidade Urbana )

	types_construction = defaultdict(float)

	for item in content:
		types_construction[item["tema"]] += float(item["negociado"])

	colors_pie = generate_colors(len(types_construction),different=True)

	# Gasto por Instituição Construtora

	institution = defaultdict(float)

	for spent in content:
		institution[spent["instituicao"]] += float(spent["negociado"])

	institution = sort_it(institution)

	institution_labels , institution_values = [] , []

	for institution,value in institution:
		institution_labels.append(institution)
		institution_values.append(value)

	background_institution , border_institution = generate_colors(len(institution_labels))

	# Gasto por tipo de instituição ( Federal , Estadual , Privada )
	# Valores e Quantidade de Obras

	types_construction_count = defaultdict(int)
	types_construction_spents = defaultdict(float)

	for spent in content:
		types_construction_count[spent["tipo_instituicao"]] += 1
		types_construction_spents[spent["tipo_instituicao"]] += float(spent["negociado"])

	colors_pie_types_construction_count = generate_colors(len(types_construction_count),different=True)
	colors_pie_types_construction_spents = generate_colors(len(types_construction_spents),different=True)

	types_spents = [sum([float(item["negociado"]) for item in content]), sum([float(item["executado"]) for item in content])]

	colors_type_spent = generate_colors(len(types_spents),different=True)


	context = {
		"label_countries" : labels,
		"values_negotiated" : values,
		"background": background,
		"border": border,

		"types_spents": types_spents,
		"colors_total_spents_type": colors_type_spent,

		"labels_type_construction": list(types_construction.keys()),
		"values_type_construction": list(types_construction.values()),
		"color_pie" : colors_pie,

		"institution_label" : institution_labels,
		"institution_values": institution_values,
		"background_institution" : background_institution,
		"border_institution": border_institution,

		"label_type_institution_count" : list(types_construction_count.keys()),
		"values_type_institution_count" : list(types_construction_count.values()),
		"color_pie_construction_count" : colors_pie_types_construction_count,

		"label_type_institution_values" : list(types_construction_spents.keys()),
		"values_type_institution_values" : list(types_construction_spents.values()),
		"color_pie_construction_values" : colors_pie_types_construction_spents
	}

	return render(request,"world-cup.html",context)