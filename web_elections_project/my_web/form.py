from django import forms

CHOICES1 = [('option1', 'Один правильный ответ'), ('option2','Несколько правильных ответов')]
CHOICES2 = []
class MyForm(forms.Form):
    text_input = forms.CharField()

    answer1 = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Введите вариант ответа:'}))
    answer2 = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Введите вариант ответа:'}))
    answer3 = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Введите вариант ответа:'}))
    answer4 = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Введите вариант ответа:'}))
    answer5 = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Введите вариант ответа:'}))
    mode = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES1)
class MultyForm (forms.Form):
    checkbox1 = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    checkbox2 = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    checkbox3 = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    checkbox4 = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    checkbox5 = forms.BooleanField(widget=forms.CheckboxInput, required=False)

class OneChoiceForm (forms.Form):
    radiobuttons = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES2)


