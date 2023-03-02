from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

        self.fields['username'].widget.attrs.update(
            {'placeholder': 'Username',
             'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update(
            {'placeholder': 'First name',
             'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update(
            {'placeholder': 'Last name',
             'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email',
                                                  'class': 'form-control'})
        self.fields['password1'].widget.attrs.update(
            {'placeholder': 'Password',
             'class': 'form-control'})
        self.fields['password2'].widget.attrs.update(
            {'placeholder': 'Password Conirmation',
             'class': 'form-control'})

    def clean_email(self):
        email = self.cleaned_data.get('email').lower().strip()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username').lower().strip()
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists')
        return username

    def clean_password2(self):
        data = self.cleaned_data
        if data['password1'] != data['password2']:
            raise forms.ValidationError('Passwords do not match')
        return data['password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username or Email:')
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'placeholder': 'Username or Email',
             'class': 'form-control form-control-lg'})
        self.fields['password'].widget.attrs.update(
            {'placeholder': 'Password',
             'class': 'form-control form-control-lg'})


class ProfileForm(forms.ModelForm):
    profile_image = forms.ImageField(widget=forms.FileInput)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'profile_image']
        
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {'placeholder': 'First name',
             'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update(
            {'placeholder': 'Last name',
             'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email',
                                                  'class': 'form-control'})
        self.fields['profile_image'].help_text = None
