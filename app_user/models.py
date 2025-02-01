from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from django.db import models

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        label="Имя",
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    age = forms.IntegerField(
        label="Возраст",
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        if commit:
            user.save()
            # Создаем или обновляем профиль пользователя
            profile, created = Profile.objects.get_or_create(user=user)
            profile.age = self.cleaned_data['age']
            profile.save()
        return user


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)  # Поле для возраста
    bio = models.TextField(blank=True, null=True)  # Поле "О себе"

    def __str__(self):
        return f'{self.user.username} Profile'