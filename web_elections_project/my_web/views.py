from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from my_web.form import MyForm, MultyForm
from my_web.models import MultyVoiceHistory, VoiceHistory
from django.contrib import messages
import datetime


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


def results(request, voice_id):
    context = {}



def voice(request, voice_id):
    context = {}
    voices = MultyVoiceHistory.objects.get(id=voice_id)

    if request.method == 'POST':
        form = MultyForm(request.POST)

        if 'checkbox1' in form.data.keys():
            answer1 = True
        else:
            answer1 = False
        if 'checkbox2' in form.data.keys():
            answer2 = True
        else:
            answer2 = False

        if 'checkbox3' in form.data.keys():
            answer3 = True
        else:
            answer3 = False

        if 'checkbox4' in form.data.keys():
            answer4 = True
        else:
            answer4 = False

        if 'checkbox5' in form.data.keys():
            answer5 = True
        else:
            answer5 = False

        if form.is_valid():
            item = VoiceHistory(
                voice_id=voice_id,
                username=request.user.username,
                answer1=answer1,
                answer2=answer2,
                answer3=answer3,
                answer4=answer4,
                answer5=answer5,
                date=datetime.datetime.now()
            )
            item.save()

            voice_count = VoiceHistory.objects.filter(voice_id=voice_id).count()

            count1 = VoiceHistory.objects.filter(voice_id=voice_id).filter(answer1=True).count() / voice_count * 100
            count2 = VoiceHistory.objects.filter(voice_id=voice_id).filter(answer2=True).count() / voice_count * 100
            count3 = VoiceHistory.objects.filter(voice_id=voice_id).filter(answer3=True).count() / voice_count * 100
            count4 = VoiceHistory.objects.filter(voice_id=voice_id).filter(answer4=True).count() / voice_count * 100
            count5 = VoiceHistory.objects.filter(voice_id=voice_id).filter(answer5=True).count() / voice_count * 100

            context['voice'] = voices
            context['voice_count'] = voice_count
            context['count1'] = count1
            context['count2'] = count2
            context['count3'] = count3
            context['count4'] = count4
            context['count5'] = count5

            return render(request, 'results.html', context)

    else:
        form = MultyForm()

    context['voice'] = voices
    context['form'] = form

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
