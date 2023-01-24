from django.shortcuts import render
from .models import Vacancy


def home(request):
	'''Функция для отображения вакансий'''
	query = Vacancy.objects.all()
	return render(request, 'scraping/home.html', {'vacancy_list': query})
