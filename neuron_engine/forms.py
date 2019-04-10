from django import forms

from .models import OriginalPost, Post, Upload


class PostForm(forms.Form):
    
    author = forms.CharField(max_length=100, required=False)
    subject = forms.CharField(max_length=100, required=False)
    text = forms.CharField(max_length=3000, widget=forms.Textarea)
    upload = forms.FileField(required=False)

    #widget=forms.ClearableFileInput(attrs={'multiple': True})
#class ThreadForm(forms.ModelForm):

#    class Meta:
#        model = OriginalPost
#        fields = ('author', 'subject', 'text')
