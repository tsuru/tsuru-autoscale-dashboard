from django import forms


def datasource_list(token):
    from datasource import client
    dl = client.list(token).json() or []
    return [(ds['Name'], ds['Name']) for ds in dl]


def action_list(token):
    from action import client
    al = client.list(token).json() or []
    return [(ds['Name'], ds['Name']) for ds in al]


class AlarmForm(forms.Form):
    name = forms.CharField()
    expression = forms.CharField()
    enabled = forms.BooleanField(initial=True)
    wait = forms.IntegerField()
    datasource = forms.ChoiceField()
    actions = forms.MultipleChoiceField()
