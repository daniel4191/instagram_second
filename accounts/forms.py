from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class SignupForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 이렇게 오버라이딩 하면, 이 필드들은 이제 필수로 입력해야하는 값이 된다.
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta(UserCreationForm.Meta):
        # UserCreationForm을 받을때, model이 정의되어 있다.
        # 하지만 해당 모델은 경로가 다르기 때문에 오버라이딩 해주자.
        # 그렇지 않으면 AttributeError at /accounts/signup/
        # Manager isn't available; 'auth.User' has been swapped for 'accounts.User'
        # 라는 에러가 뜬다.

        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    # 이메일 중복가입 방지
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            qs = User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError('이미 등록된 이메일 주소 입니다.')

        return email
