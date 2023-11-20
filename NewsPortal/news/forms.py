from django import forms
from .models import Post


class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'text']
        widgets = {
            'title': forms.TextInput(attrs={'style': 'width:275px;'}),
            'category': forms.SelectMultiple(attrs={'style': 'width:275px; height:136px;'}),
            'text': forms.Textarea(attrs={'style': 'width:400px; height:180px;'}),
        }

