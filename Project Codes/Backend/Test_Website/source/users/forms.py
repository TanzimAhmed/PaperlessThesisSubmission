from django import forms
from .models import User


class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'input', 'placeholder': 'Student ID'})


class TeacherRegistrationForm(forms.Form):
    username = forms.URLField()

    username.widget.attrs.update({'class': 'input', 'placeholder': 'North South Profile URL'})

    def clean(self):
        cleaned_data = super().clean()
        length = len(cleaned_data['username'].strip('/').split('/'))
        if ((cleaned_data['username'].find('http://ece.northsouth.edu/people/') != -1) and length != 5) or \
           ((cleaned_data['username'].find('http://www.northsouth.edu/faculty-members/') != -1) and length != 7):
            self.add_error('username', 'Please provide a Valid North South University Profile URL ')


class VerificationForm(forms.Form):
    code = forms.CharField()

    code.widget.attrs.update({'class': 'input', 'placeholder': 'Verification Code'})

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data['code'].isnumeric():
            self.add_error('code', 'Code Must be a Numeric value')
        if len(cleaned_data['code']) != 5:
            self.add_error('code', 'Code Must be a 5 Characters long')


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
