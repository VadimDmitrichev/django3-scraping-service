import codecs
import os
import sys


proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django

django.setup()

from scraping.models import City
from scraping.parsers import *


parsers = (
	(hh_ru, 'https://hh.ru/search/vacancy?text=python&area=1'),
	(habr_career, 'https://career.habr.com/vacancies?q=python&type=all'),
)
city = City.objects.filter(slug='kursk')
jobs, errors = [], []
for func, url in parsers:
	j, e = func(url)
	jobs += j
	errors += e

h = codecs.open('work.txt', 'w', 'utf-8')
h.write(str(jobs))
h.close()
