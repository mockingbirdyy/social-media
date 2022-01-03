from django import forms
from .models import Post


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '...'}),
        }