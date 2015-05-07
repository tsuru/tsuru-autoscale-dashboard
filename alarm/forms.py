from django import forms


class AlarmForm(forms.Form):
    name = forms.CharField()
