from django import forms


class AnswersForm (forms.Form):
    answer = forms.CharField(required=True)


class MyForm (forms.Form):
    form_type = forms.ChoiceField(choices=(
        (1, 'Дескретный выбор'),
        (2, "Множественный выбор")
    ), required=True)

    text_input = forms.CharField()
    answers = forms.formset_factory(AnswersForm, extra=2)


class MultyForm (forms.Form):
    response = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=[(i, '') for i in range(5)])


class RadioForm (forms.Form):
    response = forms.ChoiceField(widget=forms.RadioSelect, choices=[(i, '') for i in range(5)])
