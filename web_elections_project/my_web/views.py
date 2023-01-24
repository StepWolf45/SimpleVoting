from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from my_web.form import MyForm
from my_web.models import MultyVoiceHistory
from django.contrib import messages


def index(request):
    try:
        full_name = request.user.last_name + ' ' + request.user.first_name
    except AttributeError:
        full_name = ' '

    if full_name == ' ':
        full_name = request.user.username

    voices = MultyVoiceHistory.objects.all()

    context = {
        'full_name': full_name,
        'voices': voices
    }
    return render(request, 'main.html', context)


def voice(request, voice_id):
    context = {}
    voices = MultyVoiceHistory.objects.get(id=voice_id)
    context['voice'] = voices

    return render(request, 'voice.html', context)


def create(request):
    context = {}
    if request.method == 'POST':
        form = MyForm(request.POST)

        if form.is_valid():
            question = form.data['text_input']

            item = MultyVoiceHistory(
                question=question,
                answer1=form.data['answer1'],
                answer2=form.data['answer2'],
                answer3=form.data['answer3'],
                answer4=form.data['answer4'],
                answer5=form.data['answer5']
            )
            item.save()
    else:
        form = MyForm()

    history = MultyVoiceHistory.objects.all()
    context['history'] = history
    context['form'] = form

    return render(request, 'creating.html', context)


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
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form, 'errors': errors})


# Create your views here.
