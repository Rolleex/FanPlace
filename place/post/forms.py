
from django import forms
from .models import PostNews


class PostForm(forms.ModelForm):

    class Meta:
        model = PostNews
        fields = ('title', 'image', 'description', 'content', 'free')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea( attrs={'class': 'form-control', 'rows': 5}),
            'free': forms.CheckboxInput(attrs={'class': 'form-control'})

        }
