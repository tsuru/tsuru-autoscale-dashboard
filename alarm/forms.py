from django import forms


def datasource_list():
    from datasource import client
    dl = client.list().json() or []
    return [(ds['Name'], ds['Name']) for ds in dl]


def action_list():
    from action import client
    al = client.list().json() or []
    return [(ds['Name'], ds['Name']) for ds in al]


class AlarmForm(forms.Form):
    name = forms.CharField()
    expression = forms.CharField()
    enabled = forms.BooleanField()
    wait = forms.IntegerField()
    datasource = forms.ChoiceField(choices=datasource_list)
    actions = forms.MultipleChoiceField(choices=action_list)
