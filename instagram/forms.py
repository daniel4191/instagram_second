from django import forms

from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['photo', 'caption', 'location']
        # 특정 필드에 대한 추가 커스텀
        widgets = {
            'caption': forms.Textarea
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # 유저로부터 받고싶은 내용만
        fields = ['message']
        widgets =  {
            # TextInput은 한줄짜리다.
            # 물론 단순히 Textarea와 TextInput은 외관상 차이가 없다.
            # 하지만 커스텀이 먹는 부분에 있어서 Textarea는 기본 디폴트로 rows가 10으로 되기때문에
            # 오버라이딩이 먹는 반면, TextInput은 rows에 대한 커스텀이 먹질않는다.
            'message': forms.Textarea(attrs={'rows':2})
        }