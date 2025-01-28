from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок (необязательно)'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Содержание'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
