"""
Module used to scrape Wikipedia article traffic statistics

Results are returned in json format

Possibly be more accurate: creation date, all possible languages?
"""

import os
import csv
import requests
from datetime import date
from dateutil.relativedelta import relativedelta


# Example: 'http://stats.grok.se/json/en/201212/Seychelles'
URL_BASE = 'http://stats.grok.se/json/%(two_lang_code)s/%(date)s/%(query)s'
BASE_PATH = os.path.abspath(os.path.relpath(os.path.join(__file__, '../../../')))

# Language-country mappings
TRANSLATED_COUNTRY_NAMES = \
    csv.reader(open(os.path.join('data/auxiliary/translated_country_names.csv'), 'rb'), delimiter=',')

# Output file
OUTPUT_TSV = ''

# Languages to columns
LANGS_CORR = {'en' : 1, 'es' : 2, 'tr' : 3, 'ja' : 4, 'zh' : 5, 'it' : 6, 'fr' : 7, 'de' : 8, \
		'ru' : 9, 'nl' : 10, 'he' : 11, 'ar' : 12, 'el' : 13, 'pt' : 14, 'hi' : 15, 'ko' : 16}

END_DATE = date(2012, 12, 1)


def main():
    for language, column in LANGS_CORR.iteritems():
        for country_line in TRANSLATED_COUNTRY_NAMES:
            query = country_line[column]
            months = 0
            while True:
                dt_date = END_DATE - relativedelta(months=months)
                formatted_date = dt_date.strftime("%Y%m")
                url = URL_BASE % {'two_lang_code': language, 'date': formatted_date, 'query': query}

                req = requests.get(url)
                j = req.json()

                if not j.get('daily_views'):
                    break
                for d, view_count in j['daily_views'].iteritems():
                    print d, view_count
                months += 1


if __name__ == '__main__':
    main()
