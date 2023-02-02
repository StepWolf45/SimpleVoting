from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from my_web.form import MyForm, MultyForm, RadioForm
from my_web.models import Voices, Questions, Answers
from django.contrib import messages
import datetime


def index(request):
    try:
        full_name = request.user.last_name + ' ' + request.user.first_name
    except AttributeError:
        full_name = ' '

    if full_name == ' ':
        full_name = request.user.username

    voices = Voices.objects.all()

    context = {
        'full_name': full_name,
        'voices': voices
    }
    return render(request, 'main.html', context)


def voice(request, voice_id):
    context = {}
    form = None
    voices = Voices.objects.get(id=voice_id)
    questions = Questions.objects.filter(voice_id=voice_id)
    my_choices = questions.count()
    voice_type = voices.voice_type

    if request.method == 'POST':

        if voice_type == 'cb':
            form = MultyForm(request.POST)
            form_type = 'checkbox'

        if voice_type == 'rb':
            form = RadioForm(request.POST)
            form_type = 'radio'

        if form.is_valid():
            pass

    else:
        if voice_type == 'cb':
            form = MultyForm()
            form_type = 'checkbox'

        if voice_type == 'rb':
            form = RadioForm()
            form_type = 'radio'

    context['voice'] = voices
    context['questions'] = questions
    context['form'] = form
    context['form_type'] = form_type

    return render(request, 'voice.html', context)


def create(request):
    context = {}

    if request.method == 'POST':
        form = MyForm(request.POST)

        if request.POST.get('append'):
            form.answers.extra += 1

        if request.POST.get('create'):
            if form.is_valid():

                question = form.data['text_input']

                if form.data['form_type'] == '1':
                    voice_type = 'rb'
                else:
                    voice_type = 'cb'

                voice = Voices(
                    voice_type=voice_type,
                    author=request.user.username,
                    question=question
                )
                voice.save()
                voice_id = voice.id

                for i in range(form.answers.extra):
                    question_item = Questions(
                        voice_id=voice_id,
                        voice_type=voice_type,
                        answer_number=i,
                        answer=form.data[f'form-{i}-answer'],
                        date=datetime.datetime.now()
                    )
                    question_item.save()

            return redirect('/')

    else:
        form = MyForm()
        form.answers.extra = 2

    history = Voices.objects.all()
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
