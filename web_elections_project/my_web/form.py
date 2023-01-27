from django import forms


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
    point1 = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    point2 = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    point3 = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    point4 = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    point5 = forms.BooleanField(widget=forms.CheckboxInput, required=False)


class RadioForm (forms.Form):
    point1 = forms.BooleanField(widget=forms.RadioSelect, required=False)
    point2 = forms.BooleanField(widget=forms.RadioSelect, required=False)
    point3 = forms.BooleanField(widget=forms.RadioSelect, required=False)
    point4 = forms.BooleanField(widget=forms.RadioSelect, required=False)
    point5 = forms.BooleanField(widget=forms.RadioSelect, required=False)
