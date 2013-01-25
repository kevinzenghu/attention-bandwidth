"""
Module used to scrape Wikipedia article traffic statistics

Results are returned in json format

Possibly be more accurate: creation date, all possible languages?
"""

import os
import csv
from time import sleep
from urllib import FancyURLopener
from datetime import date
from random import randint
from BeautifulSoup import BeautifulSoup
from dateutil.relativedelta import relativedelta


BASE_PATH = os.path.abspath(os.path.relpath(os.path.join(__file__, '../../../../')))
OUTPUT = open(os.path.join(BASE_PATH, 'data/google-news/google_news_patched.tsv'), 'a')

# Language-country mappings
TRANSLATED_COUNTRY_NAMES = \
    csv.reader(open(os.path.join(BASE_PATH, 'data/auxiliary/translated_country_names.csv'), 'rb'), delimiter=',')

URL_BASE = 'https://www.google.com/search?hl={language}&tbm=nws&gl={location}&as_q={query}&as_occt=any&as_drrb=b&as_mindate={monthS}%2F{dayS}%2F{yearS}&as_maxdate={monthF}%2F{dayF}%2F{yearF}&tbs=cdr%3A1%2Ccd_min%3A{monthS}%2F{dayS}%2F{yearS}%2Ccd_max%3A{monthF}%2F{dayF}%2F{yearF}'
COUNTRY_LANGS = {'us': 'en'}
LANGS_CORR = {'en' : 1}

DATES = [date(2012, 4, 1)]

# Create a subclass of fancyurlopener that uses a specific user agent (html varies from one to another)
class gNewsOpener(FancyURLopener, object):
	version = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0; T312461)'

def check_already_scraped():
    fin = open(os.path.join(BASE_PATH, 'data/google-news/google_news_patched.tsv'))
    already_scraped = []
    for line in fin:
        dt, lang, query, _ = line.split('\t')
        already_scraped.append((dt, lang, query))
    return already_scraped


def main():
    counter = 0
    gnewsopener = gNewsOpener()
    already_scraped = check_already_scraped()
    print already_scraped
    for country, language in COUNTRY_LANGS.iteritems():
        column = LANGS_CORR[language]
        print "Country: %s Language: %s" % (country, language)

        for date in DATES:
            TRANSLATED_COUNTRY_NAMES = \
                csv.reader(open(os.path.join(BASE_PATH, 'data/auxiliary/country_names_input.csv'), 'rb'), delimiter=',')

            s_date = date
            e_date = s_date + relativedelta(months=1)
            s_year, s_month = s_date.strftime('%y'), s_date.strftime('%m')
            e_year, e_month = e_date.strftime('%y'), e_date.strftime('%m')
            output_date = '%s/1/%s' % (s_month.lstrip('0'), s_year)

            for country_line in TRANSLATED_COUNTRY_NAMES:
                country_line = country_line[0]
                query_group_list = [query_group.split('$') for query_group in country_line.split("//")]
                output_country = query_group_list[1][0]
                if (output_date, language, output_country) in already_scraped:
                    continue
                total_count = 0
                length = len(query_group_list[column])
                for query in query_group_list[column]:
                    counter += 1
                    URL = URL_BASE.format(language = language, location = country, \
                                              query = query, monthS = s_month, dayS = '1', yearS = s_year, \
                                              monthF = e_month, dayF = '1', yearF = e_year)
                    print URL

                    page = gnewsopener.open(URL)
                    soup = BeautifulSoup(page)

                    if len(soup.findAll('b')) < 3:
                        print "Captcha time!"
                    num_results = max([int(ele.getText().replace(',','')) for ele in soup.findAll('b') if ele.getText().replace(',','').isdigit()])
                    total_count += num_results

                    print "%s: %s %s" % (counter, query, num_results)

                final_results = total_count / length
                print output_country, final_results

                OUTPUT.write('%s\t%s\t%s\t%s\n' % (output_date, language, output_country, final_results))
        OUTPUT.close()

if __name__ == '__main__':
    main()
