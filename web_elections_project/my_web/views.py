from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from my_web.form import UserForm
from django.contrib import messages


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
    errors = None
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Создан аккаунт {username}!')

            return redirect('/')

        else:
            errors = list(form.errors)

            for error_index in range(len(errors)):
                if errors[error_index] == 'username':
                    errors[error_index] = 'Введен недопустимый логин!'

                if errors[error_index] == 'password2':
                    errors[error_index] = 'Такой пароль не подходит!'


    else:
        messages.error(request, 'Произошел сбой создания аккаунта.')
        form = UserForm()

    return render(request, 'register.html', {'form': form, 'errors': errors})


# Create your views here.
