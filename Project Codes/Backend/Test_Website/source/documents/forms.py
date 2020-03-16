from django import forms
from .models import Document


class DocumentForm(forms.ModelForm):
    group_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Document
        fields = ['paper']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paper'].widget.attrs.update({'placeholder': 'Upload Paper', 'class': 'input'})
