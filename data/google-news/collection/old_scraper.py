import urllib
from urllib import FancyURLopener
from random import choice
from BeautifulSoup import BeautifulSoup
import sys
from common_utils import *
import time
import os
import csv
import random
import requests
import time
from datetime import datetime, date #, time

### TODO: Need to correct for different date endianess formats!!!!
# TODO: Reorganize scrape sequence (to avoid repeating 60 identical queries)
# TODO: Refactor
#ELIMINATE REDUNDANCY FROM /12

######################################################################
# Define some variables
# Need to use xx format for year (e.g. 09, 12)
# https://www.google.com/search?hl={language}&tbm=nws&gl={location}&as_q={query}&as_occt=any&as_drrb=b&as_mindate={monthS}%2F{dayS}%2F{yearS}&as_maxdate={monthF}%2F{dayF}%2F{yearF}&tbs=cdr%3A1%2Ccd_min%3A{monthS}%2F{dayS}%2F{yearS}%2Ccd_max%3A{monthF}%2F{dayF}%2F{yearF}
URL_BASE = 'https://www.google.com/search?hl={language}&tbm=nws&gl={location}&as_q={query}&as_occt=any&as_drrb=b&as_mindate={monthS}%2F{dayS}%2F{yearS}&as_maxdate={monthF}%2F{dayF}%2F{yearF}&tbs=cdr%3A1%2Ccd_min%3A{monthS}%2F{dayS}%2F{yearS}%2Ccd_max%3A{monthF}%2F{dayF}%2F{yearF}'
#URL_BASE_LIT = 'https://www.google.com/search?hl={language}&tbm=nws&gl={location}&as_q={query}&as_occt=any&as_drrb=b&as_mindate={dayS}%2F{monthS}%2F{yearS}&as_maxdate={dayF}%2F{monthF}%2F{yearF}&tbs=cdr%3A1%2Ccd_min%3A{dayS}%2F{monthS}%2F{yearS}%2Ccd_max%3A{dayF}%2F{monthF}%2F{yearF}'
# URL_BASE = 'https://www.google.com/search?hl=%(language)s&tbm=nws&gl=%(location)s&ras_q=%(query)s&as_occt=any&as_drrb=b&as_mindate=%(monthS)s%2F%(dayS)s%2F0%(yearS)s&as_maxdate=%(monthF)s%2F%(dayF)s%2F0%(yearF)s&tbs=cdr%3A1%2Ccd_min%3A%(monthS)s%2F%(dayS)s%2F0%(yearS)s%2Ccd_max%3A%(monthF)s%2F%(dayF)s%2F0%(yearF)s'
# OUTPUT_CSV = 'gnews-with-time.csv'
COUNTRY_LANGS = {'us' : 'en' } #, 'in' : 'en', 'ng' : 'en', 'jp' : 'ja', 'hk' : 'zh-TW', 'kr' : 'ko', \
	    #'tw' : 'zh-TW', 'cn' : 'zh-CN', 'in' : 'ml', 'mx' : 'es', 'co' : 'es', 'ar' : 'es', \
		#'fr' : 'fr', 'ca' : 'fr', 'be' : 'fr', 'be' : 'nl',  'br' : 'pt-BR', 'pt' : 'pt-PT', \
		#'cz' : 'cs', 'de' : 'de', 'it' : 'it', 'hu' : 'hu', 'nl' : 'nl', 'no' : 'no', 'at' : 'de', \
		#'pl' : 'pl', 'ch' : 'de', 'se' : 'sv', 'tr' : 'tr', 'vn' : 'vi', 'gr' : 'el', 'ru' : 'ru', 'ua' : 'ru', \
		#'ua' : 'uk', 'il' : 'iw', 'in' : 'hi', 'sa' : 'ar', 'lb' : 'ar', 'eg' : 'ar' }

LANGS_CORR = {'en' : 1, 'es' : 2, 'tr' : 3, 'ja' : 4, 'it' : 5, 'zh' : 6, 'fr' : 7, 'de' : 8, \
		'ru' : 9, 'nl' : 10, 'iw' : 11, 'ar' : 12, 'el' : 13, 'pt' : 14, 'hi' : 15, 'ko' : 16, \
		'vi': 17, 'uk' : 18, 'ml' : 19, 'hu' : 20, 'no' : 21, 'pl' : 22, 'sv': 23}

PROXY_INPUT = open('proxyraw_goodconf.csv', 'r')

PROXY_LIST = PROXY_INPUT.readline().split(',')

FILENAME_BASE = 'gnews_time_output'

START_TIME = time.clock()
print "Start time: " + str(START_TIME)

# TODO: Use proxies
PROXIES = {'http' : 'http://' + '{}'.format(PROXY_LIST[random.randint(0,len(PROXY_LIST)-1)])}

# Open language-country mappings
input = open('country-names-input.csv', 'r')

# List of User Agents
# USER_AGENTS = ['Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0; T312461)']#, \
	#			'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (FM Scene 4.6.1)', \
	#			'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648)', \
	#			'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:0.9.3) Gecko/20010801', \
	#			'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/xx (KHTML like Gecko) OmniWeb/v5xx.xx']

# Create a subclass of fancyurlopener that uses a specific user agent (html varies from one to another)
class gNewsOpener(FancyURLopener, object):
	version = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0; T312461)'

# Define special exception for Captchas
class CaptchaException(Exception):
	def __init__(self):
		return
	def __str__(self):
		print "Rate Limit Exceeded"


#def getProxy():
#	try:
#	       proxy = {'http': "http://"+options.proxy}
 #       opener = urllib.FancyURLopener(proxy)
  #  except(socket.timeout):
   #     print "\n(-) Proxy Timed Out"
    #    sys.exit(1)
   # except(),msg:
    #    print "\n(-) Proxy Failed"
     #   sys.exit(1)
    #return opener



Dictionary of dates in question:
dates_dict = {'07': range(1,13), '08': range(1,13), '09': range(1,13),
 			'10': range(1,13), '11': range(1,13), '12': range(1,5)}

def writeHeader():
	# Write header of countries
	output.write("time_period")
	for line in input:
		query_group_list = [query_group[1:-1].split(',') for query_group in line.split("/")]
		output.write("," + query_group_list[1][0])

# For each language edition
for country in COUNTRY_LANGS:
	language = COUNTRY_LANGS[country]

	# Fix multiple editions in zh and pt issue, assign which column in countrynames to use
	if language == 'zh-CN' or language == 'zh-TW':
		column = LANGS_CORR['zh']
	elif language == 'pt-PT' or language ==  'pt-BR':
		column = LANGS_CORR['pt']
	elif language in LANGS_CORR:
		column = LANGS_CORR[language]
	print "Country: " + country + ", Language: " + language + ", Column: " + str(column)

	# Open new file for this edition
	outputfilename = append_to_filename(FILENAME_BASE, country + "_" + language)
	#open(outputfilename + ".csv", 'w').close()
	output = open(outputfilename, 'w')
	print "Created file: " + outputfilename

	# Write header of countries
	writeHeader()

	# Open language-country mappings
	input = open('country-names-input.csv', 'r')


	# Iterate through months
	for year, months in dates_dict.iteritems():
		for month in months:
			output.write("," + str(month) + "/1/" + year + "-")
			# Iterate through countrynames input (will be rows)
			for line in input:
				# Turn each line into a list of list of queries (can be multiple per lang)
				query_group_list = [query_group[1:-1].split(',') for query_group in line.split("/")]
				output.write(query_group_list[1][0])
				length = len(query_group_list[column])
				print "Length of group: " + str(length)
				# For every query in a list of queries
				for query in query_group_list[column]:
					gnewsopener = gNewsOpener(proxies={'http' : 'http://' + '{}'.format(PROXY_LIST[random.randint(0,len(PROXY_LIST)-1)])})
					print gnewsopener.proxies.values()[0]
					print "User Agent: " + gnewsopener.version
					print "Search query in " + language + ": " + query
					try:
						if month < 12:
							URL = URL_BASE.format(language = language, location = country, \
									query = query, monthS = month, dayS = 1, yearS = year, monthF = month + 1, \
									dayF = 1, yearF = year)
						elif month == 12:
							URL = URL_BASE.format(language = language, location = country, \
								query = query, monthS = 12, dayS = '1', yearS = year, monthF = 1, \
								dayF = '1', yearF = year_tuple[year_tuple.index(year)+1])
						page = gnewsopener.open(URL)
						#print "URL: " + URL
						soup = BeautifulSoup(page)
						print soup.findAll('b')[0:5]
						if len(soup.findAll('b')) < 3:
							print "Captcha time!"
							raise CaptchaException
						num_results = max([int(ele.getText().replace(',','')) for ele in soup.findAll('b') if ele.getText().replace(',','').isdigit()])
						if num_results > 1:
							total_count+=num_results
					except CaptchaException, IndexError:
						raise SystemExit
					except ValueError:
						PROXIES.remove(gnewsopener.proxies.values[0])
						print "Removed: " + str(gnewsopener.proxies.values[0])
						gnewsopener = gNewsOpener(proxies=PROXIES)
				print "Total count: " + str(total_count)
				average_count = total_count/length
				print "Average count: " + str(average_count)
				output.write("," + str(average_count))
			output.write("\n")
			input = open('country-names-input.csv', 'r')
END_TIME = time.clock()
print "Ended at: " + END_TIME
print "Total scrape took: " + str(END_TIME - START_TIME)
output.close()
