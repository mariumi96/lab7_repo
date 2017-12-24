# coding=utf-8
from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
_alphanumeric_validator = RegexValidator(r'^[0-9a-zA-Z_]*$',
                                         "Only alphabetic symbols, numbers and underscores allowed")

# ENABLED FORMS
class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Name, displayed to other users'}
    ), validators=[_alphanumeric_validator])
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(
        attrs={'class': 'form-control',
               'placeholder': 'your@email.com'}
    ))
    password = forms.CharField(max_length=128, widget=forms.PasswordInput(
        attrs={'class': 'form-control',
               'placeholder': '***********'}
    ))
    confirm_password = forms.CharField(max_length=128, widget=forms.PasswordInput(
        attrs={'class': 'form-control',
               'placeholder': '***********'}
    ))


    def clean(self):
        # unique email validation
        cleaned_data = super(RegisterForm, self).clean()
        if 'email' in cleaned_data:
            email = cleaned_data["email"]
            users_with_email = User.objects.filter(email=email)
            if len(users_with_email) > 0:
                raise forms.ValidationError("User with same email already registered")

        # unique username validation
        if 'username' in cleaned_data:
            username = cleaned_data["username"]
            users_with_username = User.objects.filter(username=username)
            if len(users_with_username) > 0:
                raise forms.ValidationError("User with same username already registered")

        # password confirmation validation
        if 'password' in cleaned_data:
            password = cleaned_data["password"]
            confirm_password = cleaned_data["confirm_password"]
            if not password == confirm_password:
                raise forms.ValidationError("Passwords do not match")
            return cleaned_data

    def save(self):
        new_profile = User(username=self.cleaned_data["username"],
                              email=self.cleaned_data["email"],
                              )
        new_profile.set_password(self.cleaned_data["password"])
        new_profile.save()
        return new_profile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Name, displayed to other users'}
    ), validators=[_alphanumeric_validator])
    password = forms.CharField(max_length=128, widget=forms.PasswordInput(
        attrs={'class': 'form-control',
               'placeholder': '***********'}
    ))
