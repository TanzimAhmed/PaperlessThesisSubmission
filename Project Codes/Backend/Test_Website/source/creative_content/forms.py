from django import forms
from .models import Content, Resource


class ContentForm(forms.ModelForm):
    COURSES = [
        ('CSE 499A.21', 'CSE 499A, Section 21'),
        ('CSE 499B.15', 'CSE 499B, Section 15'),
    ]

    course = forms.ChoiceField(choices=COURSES)

    class Meta:
        model = Content
        fields = ['content', 'title']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.fields['title'].widget.attrs.update({'placeholder': 'Title', 'class': 'input', 'id': 'right'})
        self.fields['content'].widget.attrs.update({'id': 'input', 'cols': 80, 'rows': 10})

    course.widget.attrs.update({'placeholder': 'Select Course', 'class': 'input', 'id': 'left'})


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['item']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item'].widget.attrs.update({'placeholder': 'Upload Paper', 'class': 'input'})