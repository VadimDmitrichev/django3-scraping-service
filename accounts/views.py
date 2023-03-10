from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from accounts.forms import UserLoginForm, UserRegistrationForm, UserUpdateForm


def login_view(request):
	"""Функция для создания пользователя"""
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		data = form.cleaned_data
		email = data.get('email')
		password = data.get('password')
		user = authenticate(request, email=email, password=password)
		login(request, user)
		return redirect('home')
	return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
	"""Функция для выхода пользователя из аккаунта"""
	logout(request)
	return redirect('home')


def register_view(request):
	"""Функция для регистрации пользователя"""
	form = UserRegistrationForm(request.POST or None)
	if form.is_valid():
		new_user = form.save(commit=False)
		new_user.set_password(form.cleaned_data['password2'])
		new_user.save()
		return render(request, 'accounts/register_done.html', {'new_user': new_user})
	return render(request, 'accounts/register.html', {'form': form})


def update_view(request):
	"""Функция для обновления данных в кабинете пользователя"""
	if request.user.is_authenticated:
		user = request.user
		if request.method == "POST":
			form = UserUpdateForm(request.POST)
		else:
			form = UserUpdateForm(initial={'city': user.city, 'language': user.language, 'send_email': user.send_email})
			return render(request, 'accounts/update.html', {'form': form})
	else:
		return redirect('accounts:login')
