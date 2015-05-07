from django import forms


class AlarmForm(forms.Form):
    name = forms.CharField()
    expression = forms.CharField()
    enabled = forms.BooleanField()
    wait = forms.IntegerField()
