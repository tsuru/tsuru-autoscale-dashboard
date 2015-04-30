from django import forms


class DataSourceForm(forms.Form):
    name = forms.CharField()
    url = forms.CharField()
    method = forms.CharField()
    body = forms.CharField()
    headers = forms.CharField()
