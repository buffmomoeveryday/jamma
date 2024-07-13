from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.exceptions import ValidationError

from .models import User


class AdminUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)


class AdminUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email",)


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        if email and password:
            try:
                user = User.objects.get(email=email)
                if not user.check_password(password):
                    raise ValidationError("Invalid email or password")
            except User.DoesNotExist:
                raise ValidationError("Invalid email or password")
        return cleaned_data


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "password"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match")

        return cleaned_data
