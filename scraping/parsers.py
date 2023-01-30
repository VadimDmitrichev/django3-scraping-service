import requests
import codecs
from bs4 import BeautifulSoup as bs
from random import randint

__all__ = ('hh_ru', 'habr_career')

# Эмуляция сервера для получения данных с сайта
headers = [
	{'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
	 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
	{
		'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
	{'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
	 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
]


def hh_ru(url, city=None, language=None):
	jobs = []
	errors = []
	if url:
		resp = requests.get(url, headers=headers[randint(0, 2)])
		if resp.status_code == 200:
			soup = bs(resp.content, 'html.parser')
			not_found_jobs = soup.find('h1', attrs={'class': 'no-content'})
			if not not_found_jobs:
				main_div = soup.find('div', attrs={'id': 'a11y-main-content'})
				if main_div:
					div_list = main_div.find_all('div', attrs={'class': 'vacancy-serp-item__layout'})
					for div_1 in div_list:
						div_title_1 = div_1.find('div', attrs={'class': 'vacancy-serp-item-body'})
						div_title_2 = div_title_1.find('div', attrs={'class': 'vacancy-serp-item-body__main-info'})
						div_with_title = div_title_2.find('div', attrs={'class': ''})
						title = div_with_title.find('h3')
						href = title.a['href']
						div_desc_1 = div_1.find('div', attrs={'class': 'g-user-content'})
						div_desc_2 = div_desc_1.find('div', attrs={'class': 'bloko-text'})
						description = div_desc_2.text
						div_company_1 = div_title_2
						div_company_2 = div_company_1.find('div', attrs={'class': 'vacancy-serp-item-company'})
						div_company_3 = div_company_2.find('div', attrs={'class': 'bloko-text'})
						div_company_4 = div_company_3.find('div',
														   attrs={'class': 'vacancy-serp-item__meta-info-company'})
						company = div_company_4.text
						jobs.append({'title': title.text, 'url': href, 'description': description, 'company': company,
									 'city_id': city, 'language_id': language}
									)
				else:
					errors.append({'url': url, 'error': 'div не найден'})
			else:
				errors.append({'url': url, 'error': 'Вакансий по данному запросу нет'})
		else:
			errors.append({'url': url, 'error': 'Страница не отвечает'})

	return jobs, errors


def habr_career(url, city=None, language=None):
	domain = 'https://career.habr.com'
	jobs = []
	errors = []
	if url:
		resp = requests.get(url, headers=headers[randint(0, 2)])
		if resp.status_code == 200:
			soup = bs(resp.content, 'html.parser')
			not_found_jobs = soup.find('div', attrs={'class': 'no-content'})
			if not not_found_jobs:
				main_div = soup.find('div', attrs={'class': 'section-group section-group--gap-medium'})
				if main_div:
					div_list = main_div.find_all('div', attrs={'class': 'vacancy-card'})
					for div_1 in div_list:
						div_title_1 = div_1.find('div', attrs={'class': 'vacancy-card__inner'})
						div_title_2 = div_title_1.find('div', attrs={'class': 'vacancy-card__info'})
						div_with_title = div_title_2.find('div', attrs={'class': 'vacancy-card__title'})
						title = div_with_title
						href = title.a['href']
						div_desc_1 = div_title_2.find('div', attrs={'class': 'vacancy-card__meta'})
						description = div_desc_1.text
						div_company_1 = div_title_2.find('div', attrs={'class': 'vacancy-card__company'})
						company = div_company_1.text
						jobs.append(
							{'title': title.text, 'url': domain + href, 'description': description, 'company': company,
							 'city_id': city, 'language_id': language}
						)
				else:
					errors.append({'url': url, 'error': 'div не найден'})
			else:
				errors.append({'url': url, 'error': 'Вакансий по данному запросу нет'})
		else:
			errors.append({'url': url, 'error': 'Страница не отвечает'})

	return jobs, errors


if __name__ == '__main__':
	url = 'https://career.habr.com/vacancies?q=python&type=all'
	jobs, errors = habr_career(url)
	h = codecs.open('work.txt', 'w', 'utf-8')
	h.write(str(jobs))
	h.close()
