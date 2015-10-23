from django import forms


OPERATOR_CHOICES = (
    ('>', '>'),
    ('>=', '>='),
    ('<=', '<='),
    ('<', '<'),
    ('!=', '!='),
)


class ScaleForm(forms.Form):
    metric = forms.ChoiceField()
    operator = forms.ChoiceField(OPERATOR_CHOICES)
    value = forms.CharField()
    step = forms.CharField(label=u'Step (in units)')
    wait = forms.IntegerField(label=u'Wait time (in seconds)')


class ConfigForm(forms.Form):
    min = forms.IntegerField(label=u'Start with units')
    process = forms.ChoiceField()
