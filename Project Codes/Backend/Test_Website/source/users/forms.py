from django import forms
from .models import User


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
