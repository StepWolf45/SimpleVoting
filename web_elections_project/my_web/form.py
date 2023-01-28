from django import forms
from my_web.models import MultyVoiceHistory


class MyForm (forms.Form):
    form_type = forms.ChoiceField(choices=(
        (1, 'Дескретный выбор'),
        (2, "Множественный выбор")
    ), required=True)

    text_input = forms.CharField()
    answer1 = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Введите вариант ответа:'}))
    answer2 = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Введите вариант ответа:'}))
    answer3 = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Введите вариант ответа:'}))
    answer4 = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Введите вариант ответа:'}))
    answer5 = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Введите вариант ответа:'}))


class MultyForm (forms.Form):
    response = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=[(i, '') for i in range(5)])


class RadioForm (forms.Form):
    response = forms.ChoiceField(widget=forms.RadioSelect, choices=[(i, '') for i in range(5)])
