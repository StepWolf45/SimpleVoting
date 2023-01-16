from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from my_web.form import UserForm
from django.contrib import messages
from django.contrib import messages
import datetime


def index(request):
    try:
        full_name = request.user.last_name + ' ' + request.user.first_name
    except AttributeError:
        full_name = ' '

    if full_name == ' ':
        full_name = request.user.username

    context = {
        'full_name': full_name,
    }
    return render(request, 'main.html', context)


def profile(request):
    return render(request, 'profile.html', {})


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Создан аккаунт {username}!')

    else:
        form = UserForm()

    return render(request, 'register.html', {'form': form})


# Create your views here.
