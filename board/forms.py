# board/forms.py

from django import forms
from .models import Post

class WriteForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '제목을 입력하세요'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': '내용을 입력하세요'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
