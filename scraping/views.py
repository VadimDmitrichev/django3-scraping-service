from django.shortcuts import render
from .forms import FindForm
from .models import Vacancy


def home(request):
	'''Функция для отображения вакансий'''

	form = FindForm()
	city = request.GET.get('city')
	language = request.GET.get('language')
	query = []
	if city or language:
		d_filter = {}
		if city:
			d_filter['city__slug'] = city
		if language:
			d_filter['language__slug'] = language
		query = Vacancy.objects.filter(**d_filter)
	return render(request, 'scraping/home.html', {'vacancy_list': query, 'form': form})
