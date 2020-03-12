from django import forms
from users.models import User
from .models import Group
from project_paperless.utils import COURSE_CHOICE_LIST


class CreateGroupForm(forms.ModelForm):
    COURSES = COURSE_CHOICE_LIST

    course = forms.ChoiceField(choices=COURSES)
    instructor = forms.CharField()
    member_1 = forms.CharField(required=False)
    member_2 = forms.CharField(required=False)
    member_3 = forms.CharField(required=False)
    member_4 = forms.CharField(required=False)
    member_5 = forms.CharField(required=False)

    class Meta:
        model = Group
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': 'Group Name', 'class': 'input'})
        self.username = None

    course.widget.attrs.update({'placeholder': 'Select Course', 'class': 'input'})
    instructor.widget.attrs.update({'placeholder': 'Instructor ID', 'class': 'input'})
    member_1.widget.attrs.update({'placeholder': "Member 1", 'class': 'input'})
    member_2.widget.attrs.update({'placeholder': "Member 2", 'class': 'input'})
    member_3.widget.attrs.update({'placeholder': "Member 3", 'class': 'input'})
    member_4.widget.attrs.update({'placeholder': "Member 4", 'class': 'input'})
    member_5.widget.attrs.update({'placeholder': "Member 5", 'class': 'input'})

    def set_user(self, username):
        self.username = username

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['members'] = []
        try:
            cleaned_data['instructor'] = User.objects.get(username=cleaned_data['instructor'])
        except User.DoesNotExist:
            self.add_error('instructor', f"Instructor ID: {cleaned_data['instructor']} is not Registered.")
        for i in range(1, 6):
            if cleaned_data[f'member_{i}']:
                if self.username == cleaned_data[f'member_{i}']:
                    self.add_error(f'member_{i}', f"Your ID is automatically included, Do not include here.")
                    continue
                try:
                    member = User.objects.get(username=cleaned_data[f'member_{i}'])
                except User.DoesNotExist:
                    self.add_error(f'member_{i}', f"Student ID: {cleaned_data[f'member_{i}']} is not Registered.")
                else:
                    if member in cleaned_data['members']:
                        self.add_error(f'member_{i}', f"Student ID: {cleaned_data[f'member_{i}']} is entered before.")
                    cleaned_data['members'].append(member)


class GroupSelectForm(forms.Form):
    GROUPS = []

    groups = forms.ChoiceField(choices=GROUPS)

    def update_choice(self, user):
        self.GROUPS = []
        groups = user.group_set.all()
        for group in groups:
            self.GROUPS.append((group.id, group.get_string()))
        self.fields['groups'].choices = self.GROUPS

    def update_initial_choice(self, choice):
        self.fields['groups'].initial = choice
