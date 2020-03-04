from django import forms
from .models import User, Group


class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'] = forms.CharField(widget=forms.PasswordInput)
        self.fields['username'].widget.attrs.update({'class': 'input', 'placeholder': 'Student ID'})
        self.fields['first_name'].widget.attrs.update({'class': 'input', 'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'class': 'input', 'placeholder': 'Last Name'})
        self.fields['email'].widget.attrs.update({'class': 'input', 'placeholder': 'NSU E-mail Address'})
        self.fields['password'].widget.attrs.update({'class': 'input', 'placeholder': 'Password'})

    confirm_password.widget.attrs.update({'class': 'input', 'placeholder': 'Confirm Password'})

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirmation = cleaned_data['confirm_password']

        if password != confirmation:
            self.add_error('password', 'Password does not match with the confirmation field')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    username.widget.attrs.update({'class': 'input', 'placeholder': 'Student ID'})
    password.widget.attrs.update({'class': 'input', 'placeholder': 'Password'})


class CreateGroupForm(forms.ModelForm):
    COURSES = [
        ('CSE 499A.21', 'CSE 499A, Section 21'),
        ('CSE 499B.15', 'CSE 499B, Section 15'),
    ]

    course = forms.ChoiceField(choices=COURSES)
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
