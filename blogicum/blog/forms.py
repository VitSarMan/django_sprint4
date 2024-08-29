from django import forms

from .models import Post, Comments


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'text', 'category', 'location', 'image', 'pub_date']
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


class CommentsForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ['text']
