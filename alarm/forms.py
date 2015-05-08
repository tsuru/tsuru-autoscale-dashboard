from django import forms


def datasource_list():
    from datasource import client
    return [(ds['Name'], ds['Name']) for ds in client.list().json()]


def action_list():
    from action import client
    return [(ds['Name'], ds['Name']) for ds in client.list().json()]


class AlarmForm(forms.Form):
    name = forms.CharField()
    expression = forms.CharField()
    enabled = forms.BooleanField()
    wait = forms.IntegerField()
    datasource = forms.ChoiceField(choices=datasource_list)
    actions = forms.MultipleChoiceField(choices=action_list)
