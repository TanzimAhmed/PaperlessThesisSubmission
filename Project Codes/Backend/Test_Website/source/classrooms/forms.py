from django import forms
from .models import Classroom, Quiz, Question
from project_paperless.utils import COURSE_CHOICE_LIST, SEMESTER_CHOICE_LIST


class CreateClassForm(forms.ModelForm):
    course = forms.ChoiceField(choices=COURSE_CHOICE_LIST)

    class Meta:
        model = Classroom
        fields = ['name', 'semester']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['semester'] = forms.ChoiceField(choices=SEMESTER_CHOICE_LIST)
        self.fields['name'].widget.attrs.update({'placeholder': 'Class Name', 'class': 'input'})
        self.fields['semester'].widget.attrs.update({'placeholder': 'Select Semester', 'class': 'input'})

    course.widget.attrs.update({'placeholder': 'Select Course', 'class': 'input'})


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'due_date', 'is_open']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'placeholder': 'Quiz Title', 'class': 'input'})
        self.fields['due_date'].widget.attrs.update({'placeholder': 'Due Date', 'class': 'input'})
        self.fields['is_open'].widget.attrs.update({'placeholder': 'Open Quiz', 'class': 'input'})


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'options', 'answer', 'points', 'time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'placeholder': 'Question Text', 'id': 'question'})
        self.fields['options'].widget.attrs.update({'placeholder': 'Choices', 'id': 'options'})
        self.fields['answer'].widget.attrs.update({'placeholder': 'Correct Choice', 'class': 'input'})
        self.fields['points'].widget.attrs.update({'placeholder': 'Points', 'class': 'input'})
        self.fields['time'].widget.attrs.update({'placeholder': 'Time (in seconds)', 'class': 'input'})


class JoinClassForm(forms.Form):
    classroom = forms.CharField()

    classroom.widget.attrs.update({'placeholder': 'Class Code', 'class': 'input'})


class TakeQuizForm(forms.Form):
    answers = forms.CharField(widget=forms.HiddenInput)
