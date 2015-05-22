from django import forms


class ScaleForm(forms.Form):
    metric = forms.ChoiceField()
    operator = forms.ChoiceField()
    value = forms.CharField()
    units = forms.CharField()
    wait = forms.IntegerField()
