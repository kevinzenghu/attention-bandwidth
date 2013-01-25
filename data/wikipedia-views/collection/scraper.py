"""
Module used to scrape Wikipedia article traffic statistics

Results are returned in json format

Possibly be more accurate: creation date, all possible languages?
"""

import os
import csv
import requests
from time import sleep
from datetime import date
from random import randint
from dateutil.relativedelta import relativedelta


# Example: 'http://stats.grok.se/json/en/201212/Seychelles'
URL_BASE = 'http://stats.grok.se/json/%(two_lang_code)s/%(date)s/%(query)s'
BASE_PATH = os.path.abspath(os.path.relpath(os.path.join(__file__, '../../../../')))
OUTPUT = open(os.path.join(BASE_PATH, 'data/wikipedia-views/wikipedia_views_1-18-2013.tsv'), 'a')

# Language-country mappings
TRANSLATED_COUNTRY_NAMES = \
    csv.reader(open(os.path.join(BASE_PATH, 'data/auxiliary/translated_country_names.csv'), 'rb'), delimiter=',')

# Output file
OUTPUT_TSV = ''

# Languages to columns
LANGS_CORR = {'en' : 1, 'es' : 2, 'tr' : 3, 'ja' : 4, 'zh' : 5, 'it' : 6, 'fr' : 7, 'de' : 8, \
		'nl' : 10, 'he' : 11, 'ar' : 12, 'el' : 13, 'pt' : 14, 'hi' : 15, 'ko' : 16}

END_DATE = date(2012, 12, 1)


def any_nonzero(di):
    for v in di.values():
        if v:
            return True
    return False


def check_already_scraped():
    fin = open(os.path.join(BASE_PATH, 'data/wikipedia-views/wikipedia_views_1-18-2013.tsv'))
    already_scraped = []
    for line in fin:
        dt, lang, query, _ = line.split('\t')
        year, month, _ = dt.split('-')
        year, month = int(year), int(month)
        already_scraped.append((date(year, month, 1), lang, query))
    return already_scraped


def main():
    already_scraped = check_already_scraped()

    for language, column in LANGS_CORR.iteritems():
        TRANSLATED_COUNTRY_NAMES = \
            csv.reader(open(os.path.join(BASE_PATH, 'data/auxiliary/translated_country_names.csv'), 'rb'), delimiter=',')
        _unused = TRANSLATED_COUNTRY_NAMES.next()

        for country_line in TRANSLATED_COUNTRY_NAMES:
            di = dict()
            query = country_line[column]
            months = 0
            while True:
                dt_date = END_DATE - relativedelta(months=months)
                if (dt_date, language, country_line[1]) in already_scraped:
                    break
                print (dt_date, language, country_line[1])
                delay = float(randint(1, 100))/500
                print delay
                sleep(delay)
                formatted_date = dt_date.strftime("%Y%m")
                url = URL_BASE % {'two_lang_code': language, 'date': formatted_date, 'query': query}
                print url

                req = requests.get(url)
                j = req.json

                if not any_nonzero(j.get('daily_views')):
                    print j
                    for dt in sorted(di.keys()):
                        OUTPUT.write('%s\t%s\t%s\t%s\n' % \
                                         (dt, language, country_line[1], di[dt]))
                    break

                for d, view_count in j['daily_views'].iteritems():
                    di[d] = view_count
                months += 1
    OUTPUT.close()

if __name__ == '__main__':
    main()
