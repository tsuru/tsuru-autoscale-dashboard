from django import forms


class ScaleUpForm(forms.Form):
    metric = forms.ChoiceField()
    operator = forms.ChoiceField()
    value = forms.CharField()
    units = forms.CharField()
    wait = forms.IntegerField()
