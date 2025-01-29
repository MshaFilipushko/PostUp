from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    captcha = CaptchaField(label="Пожалуйста, докажите, что вы человек")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "captcha")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


