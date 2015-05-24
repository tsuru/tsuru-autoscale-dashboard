from django import forms


OPERATOR_CHOICES = (
    ('>', '>'),
    ('>=', '>='),
    ('<=', '<='),
    ('<', '<'),
    ('!=', '!='),
)


METRIC_CHOICES = (
    ('cpu', 'cpu'),
    ('memory', 'memory'),
    ('request/min', 'request/min'),
    ('response time', 'response time'),
)


class ScaleForm(forms.Form):
    metric = forms.ChoiceField(METRIC_CHOICES)
    operator = forms.ChoiceField(OPERATOR_CHOICES)
    value = forms.CharField()
    units = forms.CharField(label=u'Step (in units)')
    wait = forms.IntegerField(label=u'Wait time (in seconds)')


class ConfigForm(forms.Form):
    min = forms.IntegerField(label=u'Start with units')
