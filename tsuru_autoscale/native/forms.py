from django import forms


class ScaleForm(forms.Form):
    process = forms.ChoiceField(label=u'Process',
                                widget=forms.Select(attrs={'class': 'form-control'}))
    min_units = forms.IntegerField(label=u'Min units', min_value=1, initial=2,
                                   widget=forms.NumberInput(attrs={'class': 'form-control'}))
    max_units = forms.IntegerField(label=u'Max units', min_value=2, initial=2,
                                   widget=forms.NumberInput(attrs={'class': 'form-control'}))
    target_cpu = forms.IntegerField(label=u'Target CPU %', min_value=10, initial=50,
                                    max_value=90,
                                    widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super(ScaleForm, self).clean()
        min_units = cleaned_data.get("min_units")
        max_units = cleaned_data.get("max_units")

        if min_units >= max_units:
            self.add_error('max_units', "Max units should be greater than min units.")
