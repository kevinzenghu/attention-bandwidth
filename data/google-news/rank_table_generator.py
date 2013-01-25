# For Google News Dataset

import datetime
import simplejson as json
from pprint import pprint


fin_name = 'gnews_monthly_us_mx_cn_2012-04-21_augmented.csv'
fin = open(fin_name)
fin.readline()

fout = open(fin_name.split('.')[0] + '.tsv', 'w')

final_dict = {}
countries_dict = {}
dates = []
num_results_dict = {}
ranking_dict = {}

for line in fin:
    date, _, _, _, lang, country, num_results = line.split(',')
    if lang != 'en':
        break
    month, day, year = date.split('/')
    month, day, year = int(month), int(day), int('20' + year)
    num_results = int(num_results.strip())
    d = datetime.date(year, month, day).strftime('%Y-%m-%d')

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

fout.write('Country\t')
dates = sorted(dates)
fout.write('\t'.join(dates) + '\n')

countries_list = []

countries_sorted = sorted(countries_dict)
for country in countries_sorted:
    v = countries_dict[country]
    fout.write(country)
    for date in dates:
        fout.write('\t%s' % v[date])
    fout.write('\n')

fout.close()
