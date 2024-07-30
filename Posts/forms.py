from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image', 'video']

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)