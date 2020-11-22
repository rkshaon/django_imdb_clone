from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from authy.models import Profile

def ForbiddenUsers(value):
    forbidden_users = ['admin', 'css', 'js', 'authenticate', 'login', 'logout',
    'root', 'administrator', 'email', 'join', 'sql', 'insert', 'db', 'static', 'python',
    'delete', 'TABLE', 'insert']

    if value.lower() in forbidden_users:
        raise ValidationError('Invalid name for user, this is a reserved word.')

def InvalidUser(value):
    if '@' in value or '+' in value or '-' in value:
        raise ValidationError('This is invalid user, do not user this characters: @, +, -')

def UniqueEmail(value):
    if User.objects.filter(email_iexact=value).exists():
        raise ValidationError('User with this e-mail already exists.')

def UniqueUser(value):
    if User.objects.filter(username_iexact=value).exists():
        raise ValidationError('User with this username already exists.')

class SignUp(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(), max_length=30, required=True)
    email = forms.CharField(widget=forms.EmailInput(), max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True, label='Confirm your password.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        
