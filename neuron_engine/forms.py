from django import forms

from .models import OriginalPost, Post, Upload


class PostForm(forms.Form):
    
    author = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class':'textinput','placeholder':'Автор'}),
        )
    subject = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class':'textinput','placeholder':'Тема'}),
        )
    text = forms.CharField(
        max_length=3000,
        widget=forms.Textarea(attrs={'class':'textarea','placeholder':'Текст сообщения'}),
        )
    upload = forms.FileField(required=False)
