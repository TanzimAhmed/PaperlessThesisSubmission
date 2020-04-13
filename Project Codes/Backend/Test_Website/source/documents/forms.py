from django import forms
from .models import Document


class DocumentForm(forms.ModelForm):
    group_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Document
        fields = ['title', 'paper']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'placeholder': 'Paper Title', 'class': 'input'})
        self.fields['paper'].widget.attrs.update({'placeholder': 'Upload Paper', 'class': 'input'})
