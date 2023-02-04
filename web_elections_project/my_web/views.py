from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from my_web.form import MyForm, MultyForm, RadioForm
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


def voice(request, voice_id):
    context = {}
    form = None
    voices = MultyVoiceHistory.objects.get(id=voice_id)
    voice_type = voices.voice_type
    if request.method == 'POST':

        if voice_type == 'cb':
            form = MultyForm(request.POST)
            form_type = 'checkbox'

        if voice_type == 'rb':
            form = RadioForm(request.POST)
            form_type = 'radio'

        if form.is_valid():
            response = dict(form.data)['response']
            value_list = [False] * 5

            for i in range(5):
                if str(i) in response:
                    value_list[i] = True

            item = VoiceHistory(
                voice_id=voice_id,
                voice_type=voice_type,
                username=request.user.username,
                answer1=value_list[0],
                answer2=value_list[1],
                answer3=value_list[2],
                answer4=value_list[3],
                answer5=value_list[4],
                date=datetime.datetime.now()
            )
            item.save()

            voice_count = VoiceHistory.objects.filter(voice_id=voice_id).count()
            voice_history = VoiceHistory.objects.filter(voice_id=voice_id)

            count1 = round((voice_history.filter(answer1=True).count() / voice_count) * 100, 2)
            count2 = round((voice_history.filter(answer2=True).count() / voice_count) * 100, 2)
            count3 = round((voice_history.filter(answer3=True).count() / voice_count) * 100, 2)
            count4 = round((voice_history.filter(answer4=True).count() / voice_count) * 100, 2)
            count5 = round((voice_history.filter(answer5=True).count() / voice_count) * 100, 2)

            context['voice'] = voices
            context['voice_count'] = voice_count
            context['count1'] = count1
            context['count2'] = count2
            context['count3'] = count3
            context['count4'] = count4
            context['count5'] = count5

            return render(request, 'results.html', context)

    else:
        if voice_type == 'cb':
            form = MultyForm()
            form_type = 'checkbox'

        if voice_type == 'rb':
            form = RadioForm()
            form_type = 'radio'

    context['voice'] = voices
    context['form'] = form
    context['form_type'] = form_type

    return render(request, 'voice.html', context)


def create(request):
    context = {}
    if request.method == 'POST':
        form = MyForm(request.POST)

        if form.is_valid():
            question = form.data['text_input']

            if form.data['form_type'] == '1':
                voice_type = 'rb'
            else:
                voice_type = 'cb'

            item = MultyVoiceHistory(
                question=question,
                voice_type=voice_type,
                author=request.user.username,
                answer1=form.data['answer1'],
                answer2=form.data['answer2'],
                answer3=form.data['answer3'],
                answer4=form.data['answer4'],
                answer5=form.data['answer5']
            )
            item.save()

            return redirect('/')
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
                    errors[error_index] = ''
                    errors.append('Пароль должен состоять минимум из 8 символов.')
                    errors.append('Пароль не должен содержать личную информацию.')
                    errors.append('Пароль не должен состоять только из цифр.')
                    errors.append('Пароль не должен быть широко используемым.')


    else:
        messages.error(request, 'Произошел сбой создания аккаунта.')
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form, 'errors': errors})


# Create your views here.
