# For Google News Dataset

import datetime
import simplejson as json
from pprint import pprint


fin_name = 'wikipedia_weekly_1-24-2013.tsv'
fin = open(fin_name)
fin.readline()

fout = open(fin_name.split('.')[0] + '.js', 'w')

final_dict = {}
countries_dict = {}
dates = []
num_results_dict = {}
ranking_dict = {}

for line in fin:
    d, lang, country, num_results = line.split('\t')
    if lang != 'en':
        continue

    num_results = int(num_results.strip())

    if d not in num_results_dict:
        num_results_dict[d] = {country: num_results}
    else:
        num_results_dict[d].update({country: num_results})

    if d not in dates:
        dates.append(d)

for d, v in num_results_dict.iteritems():
    ranking_dict[d] = {}
    intermediate_dict = {}
    sorted_countries = sorted(v.keys(), key=lambda k: v[k], reverse=True)
    for country in sorted_countries:
        ranking_dict[d][country] = sorted_countries.index(country)

for d, v in ranking_dict.iteritems():
    for country, rank in v.iteritems():
        rank += 1
        if country not in countries_dict:
            countries_dict[country] = {d: rank}
        else:
            countries_dict[country].update({d: rank})

dates = sorted(dates)

countries_list = []
for country, v in countries_dict.iteritems():
    if len(v) != 263:
        continue
    intermediate_dict = {}
    intermediate_dict['country'] = country
    for date in dates:
        intermediate_dict[date] = v[date]
    countries_list.append(intermediate_dict)

countries_list = sorted(countries_list, key = lambda k: k['2007-12-16'])

final_dict['countries'] = countries_list

j = json.dumps(final_dict, sort_keys=True)

fout.write("var wiki = "+j+";")
fout.close()
