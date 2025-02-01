from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from django.db import models

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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)  # Поле для возраста
    bio = models.TextField(blank=True, null=True)  # Поле "О себе"

    def __str__(self):
        return f'{self.user.username} Profile'