from django import forms
from .models import Candidate

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ('cid', 'name', 'designation')

    def __init__(self, *args, **kwargs):
        self.edit = kwargs.pop('edit', False)
        super(CandidateForm, self).__init__(*args, **kwargs)
        if self.edit:
            self.fields.pop('cid')

    def clean_name(self):
        data = self.cleaned_data.get("name").title()
        return data
