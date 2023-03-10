import jsonfield
from django.db import models

from scraping.utils import from_cyrillic_to_eng


def default_urls():
	return {'hh_ru': '', 'habr_career': ''}


class City(models.Model):
	name = models.CharField(max_length=100,
							verbose_name='Город',
							unique=True)
	slug = models.CharField(max_length=100, blank=True)

	class Meta:
		verbose_name = 'Город'
		verbose_name_plural = 'Города'

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = from_cyrillic_to_eng(str(self.name))
		super().save(*args, **kwargs)


class Language(models.Model):
	name = models.CharField(max_length=100,
							verbose_name='Язык программирования',
							unique=True)
	slug = models.CharField(max_length=100, blank=True)

	class Meta:
		verbose_name = 'Язык программирования'
		verbose_name_plural = 'Языки программирования'

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = from_cyrillic_to_eng(str(self.name))
		super().save(*args, **kwargs)


class Vacancy(models.Model):
	url = models.URLField(unique=True)
	title = models.CharField(max_length=250, verbose_name='Название вакансии')
	company = models.CharField(max_length=250, verbose_name='Компания')
	description = models.TextField(verbose_name='Описание вакансии')
	city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город')
	language = models.ForeignKey('Language', on_delete=models.CASCADE, verbose_name='Язык программирования')
	timestamp = models.DateField(auto_now_add=True)

	class Meta:
		verbose_name = 'Вакансия'
		verbose_name_plural = 'Вакансии'
		ordering = ['-timestamp']

	def __str__(self):
		return self.title


class Error(models.Model):
	"""Модель для формирования ошибок связанных с парсингом"""
	timestamp = models.DateField(auto_now_add=True)
	data = jsonfield.JSONField()

	class Meta:
		verbose_name = 'Ошибка'
		verbose_name_plural = 'Ошибки'

	def __str__(self):
		return self.title


class Url(models.Model):
	"""Модель для формирования уникальных url"""
	city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город')
	language = models.ForeignKey('Language', on_delete=models.CASCADE, verbose_name='Язык программирования')
	url_data = jsonfield.JSONField(default=default_urls)

	class Meta:
		unique_together = ('city', 'language')
		verbose_name= 'Ссылка'
		verbose_name_plural= 'Ссылки'
