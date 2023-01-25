from django import forms

from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['photo', 'caption', 'location']
        # 특정 필드에 대한 추가 커스텀
        widgets = {
            'caption': forms.Textarea
        }