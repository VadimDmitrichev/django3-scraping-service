from django.core.paginator import Paginator
from django.shortcuts import render
from .forms import FindForm
from .models import Vacancy


def home(request):
	"""Функция для отображения вакансий"""

	form = FindForm()

	return render(request, 'scraping/home.html', {'form': form})


def list_view(request):
	"""Функция для отображения вакансий"""
	page_obj = None
	form = FindForm()
	city = request.GET.get('city')
	language = request.GET.get('language')
	query = []
	context = {
		'city': city,
		'language': language,
		'form': form
	}
	if city or language:
		d_filter = {}
		if city:
			d_filter['city__slug'] = city
		if language:
			d_filter['language__slug'] = language
		query = Vacancy.objects.filter(**d_filter)
		paginator = Paginator(query, 10)
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)
		context['vacancy_list'] = page_obj
	return render(request, 'scraping/list_view.html', context)
