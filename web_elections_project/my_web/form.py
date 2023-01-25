from django import forms


class MyForm (forms.Form):
    text_input = forms.CharField()

    answer1 = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Введите вариант ответа:'}))
    answer2 = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Введите вариант ответа:'}))
    answer3 = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Введите вариант ответа:'}))
    answer4 = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Введите вариант ответа:'}))
    answer5 = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Введите вариант ответа:'}))


class MultyForm (forms.Form):
    checkbox1 = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    checkbox2 = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    checkbox3 = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    checkbox4 = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    checkbox5 = forms.BooleanField(widget=forms.CheckboxInput, required=False)
