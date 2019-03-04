from django import forms
from .models import Candidate, Comment

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

class CommentForm (forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('title', 'text', 'type', 'starred')

    def __init__(self, request=None, *args, **kwargs):
        if request:
            super(CommentForm, self).__init__(request.POST, *args, **kwargs)
        else:
            super(CommentForm, self).__init__(*args, **kwargs)
