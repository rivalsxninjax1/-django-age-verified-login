# myapp/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].help_text = None  # Remove the help texts

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'autocomplete': 'off', 'placeholder': 'Username'}),
        help_text=''  # Remove default help text
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'autocomplete': 'off', 'placeholder': 'Email address'}),
        help_text=''  # Remove default help text
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'off', 'placeholder': 'Password'}),
        help_text=''  # Remove default password help text
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'autocomplete': 'off', 'placeholder': 'Confirm password'}),
        help_text=''  # Remove password confirmation help text
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # Remove help texts and errors
        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].help_text = None

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        # Custom password validation without unnecessary messages
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn’t match.")
        if len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password2
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')