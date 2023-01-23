from django.db import models

from scraping.utils import from_cyrillic_to_eng


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
