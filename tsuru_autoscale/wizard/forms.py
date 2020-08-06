from django import forms


OPERATOR_CHOICES = (
    ('>', '>'),
    ('>=', '>='),
    ('<=', '<='),
    ('<', '<'),
    ('!=', '!='),
)


AGGREGATOR_CHOICES = (
    ('avg', 'average'),
    ('max', 'maximum'),
)


class ScaleForm(forms.Form):
    metric = forms.ChoiceField()
    aggregator = forms.ChoiceField(AGGREGATOR_CHOICES)
    operator = forms.ChoiceField(OPERATOR_CHOICES)
    value = forms.IntegerField(min_value=0)
    step = forms.IntegerField(label=u'Step (in units)', min_value=1, initial=1)
    wait = forms.IntegerField(label=u'Wait time (in seconds)')

    def __init__(self, min_wait, *args, **kwargs):
        super(ScaleForm, self).__init__(*args, **kwargs)
        self.fields['wait'] = forms.IntegerField(label=u'Wait time (in seconds)', min_value=min_wait, initial=min_wait)

    def clean_value(self):
        return str(self.cleaned_data.get('value'))

    def clean_step(self):
        return str(self.cleaned_data.get('step'))


class ConfigForm(forms.Form):
    min = forms.IntegerField(label=u'Start with units', min_value=2, initial=2)
    process = forms.ChoiceField()
