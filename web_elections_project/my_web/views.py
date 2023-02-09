from django.contrib.auth.forms import UserCreationForm
from django.forms import formset_factory
from django.shortcuts import render, redirect
from my_web.form import MyForm, MultyForm, RadioForm, AnswersSet
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
    voice_type = voices.voice_type

    answers_choices = [
        (question.answer_number, question.answer) for question in questions
    ]

    if request.method == 'POST':
        if voice_type == 'cb':
            form = MultyForm(request.POST)
        if voice_type == 'rb':
            form = RadioForm(request.POST)
        form.fields['response'].choices = answers_choices

        if form.is_valid():
            answer = form.cleaned_data.get('response')
            answers_list = [
                [choice, False] for choice in range(len(answers_choices))
            ]

            for i in range(len(answers_list)):
                if str(i) in answer:
                    answers_list[i][1] = True

            context['answer'] = answers_list

            for item in answers_list:
                answer_db = Answers(
                    voice_id=voice_id,
                    answer_number=item[0],
                    author=request.user.username,
                    answer=item[1],
                    date=datetime.datetime.now()
                )
                answer_db.save()

            answers = Answers.objects.filter(voice_id=voice_id)

            voiced_people = answers.count() // questions.count()

            answers_list = []

            for i in range(questions.count()):
                current_voice = answers.filter(answer_number=i)
                voiced_true = current_voice.filter(answer=True).count()
                voice_num = round(voiced_true / current_voice.count(), 2) * 100

                question = questions.get(answer_number=i).answer

                answers_list.append(
                    (question, voice_num)
                )

            context['voice'] = voices
            context['voiced_people'] = voiced_people
            context['answers_list'] = answers_list

            return render(request, 'results.html', context)

    else:
        if voice_type == 'cb':
            form = MultyForm()
        if voice_type == 'rb':
            form = RadioForm()
        form.fields['response'].choices = answers_choices

    context['voice'] = voices
    context['form'] = form

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

                if dict(request.FILES) == {}:
                    voice = Voices(
                        voice_type=voice_type,
                        author=request.user.username,
                        question=question,
                    )
                else:
                    voice = Voices(
                        voice_type=voice_type,
                        author=request.user.username,
                        question=question,
                        voice_picture=request.FILES['voice_picture']
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
    context = {}
    voices = Voices.objects.filter(author=request.user.username)
    context['voices'] = voices
    return render(request, 'profile.html', context)


def change(request, voice_id):
    context = {'voices': voice_id}

    voices = Voices.objects.get(id=voice_id)
    questions = Questions.objects.filter(voice_id=voice_id)

    if request.method == 'POST':
        change_form = MyForm(
            request.POST,
            initial={
                'text_input': voices.question,
                'form_type': voices.voice_type,
            }
        )

        if request.POST.get('append'):
            change_form.answers.extra += 1

        change_form.answers = change_form.answers(
            initial=[
                {'answer': i.answer} for i in questions
            ]
        )

        if request.POST.get('create'):
            if change_form.is_valid():
                Questions.objects.filter(voice_id=voice_id).delete()
                Answers.objects.filter(voice_id=voice_id).delete()

                voice_mod = Voices.objects.get(id=voice_id)

                question = change_form.data['text_input']

                if change_form.data['form_type'] == '1':
                    voice_type = 'rb'
                else:
                    voice_type = 'cb'

                voice_mod.question = question
                voice_mod.voice_type = voice_type
                voice_mod.save()

                for i in range(change_form.answers.extra + questions.count()):
                    question_item = Questions(
                        voice_id=voice_id,
                        voice_type=voice_type,
                        answer_number=i,
                        answer=change_form.data[f'form-{i}-answer'],
                        date=datetime.datetime.now()
                    )
                    question_item.save()

            return redirect('/')

    else:
        change_form = MyForm(
            initial={
                'text_input': voices.question,
                'form_type': voices.voice_type,
            }
        )

        change_form.answers.extra = 1

        change_form.answers = change_form.answers(
            initial=[
                {'answer': i.answer} for i in questions
            ]
        )

    context['question'] = voices.question
    context['voice_type'] = voices.voice_type
    context['voice_picture'] = voices.voice_picture
    context['change_form'] = change_form

    return render(request, 'change.html', context)


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
