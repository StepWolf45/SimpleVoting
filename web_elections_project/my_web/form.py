from django import forms


class AnswersForm (forms.Form):
    answer = forms.CharField(required=True,widget=forms.TextInput(
                              attrs={'class': "text_field_input"}))


class MyForm (forms.Form):
    form_type = forms.ChoiceField(choices=(
        (1, 'Дискретный выбор'),
        (2, "Множественный выбор")
    ), required=True)

    voice_picture = forms.FileField(
        required=False
    )

    text_input = forms.CharField(widget=forms.TextInput(attrs={'class': "text_field_input"}))
    answers = forms.formset_factory(AnswersForm)


class MultyForm (forms.Form):
    response = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, choices=[]
    )


class RadioForm (forms.Form):
    response = forms.ChoiceField(
        widget=forms.RadioSelect, choices=[]
    )
