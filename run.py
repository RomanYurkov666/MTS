#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import confluence
import smtplib
import datetime
import codecs


reload(sys)
sys.setdefaultencoding('utf-8')

from bs4 import BeautifulSoup
from config import *

""" 
Function which check people for who working now in compony and near birthday's of worker's
"""

def is_correct(x):
	if x['room'] == u'\u0443\u0432\u043e\u043b\u0435\u043d':
		return False
	try:
		birthday = datetime.datetime.strptime(x['bd_date'] + 
			'.{}'.format(datetime.datetime.now().year),'%d.%m.%Y')
	except ValueError:
		return False
	ftime = datetime.datetime.now() + datetime.timedelta(days=7)
	
	if datetime.datetime.now() <=birthday <= ftime:
		return True

	return False

if __name__ == "__main__":

# Parsing confluence html page with worker's table to dictionary 

	api = confluence.Api(URL, USER, PASSWORD)
	html_data = api.getpagecontent(PAGE_NAME, SPACE_NAME)

	with codecs.open("list.html", "w", encoding = 'utf-8') as f:
		f.write (html_data)

	table_data = [[cell.text for cell in row("td")]
	                         for row in BeautifulSoup(html_data)("tr")]
	
	mapper = [
		'number', 
		'fi', 
		'job',
	    'fio',
		'email',
		'ip',
		'phone',
		'bd_date',
		'loginAD',
		'room',
		'email_alias',
		't_num']

	table_data = [dict(zip(mapper, x)) for x in table_data if len(x) == len(mapper)]
	haveBD_data = [x for x in table_data if is_correct(x)]
	
#Initialaze SMTP server and formation mail to send
 	s = smtplib.SMTP(SMTP_SERVER_HOST)

	for i in haveBD_data:
		to_addrs = [x['email'] for x in table_data if x['number'] != i['number']]

		print to_addrs

# Uncomment this function to send mail

		"""s.sendmail(
			MY_EMAIL_ADDR, 
			to_addrs, 
			MSG.format(username=i['fio'], dt=i['bd_date'])
		)"""
		print MSG.format(username=i['fio'], dt=i['bd_date'])
	

	s.quit()
