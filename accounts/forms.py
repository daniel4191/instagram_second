from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User

# 이건 올바른 User form 생성이 아니다.
# 왜냐하면 password가 암호화 되지 않기 때문이다.
# 이에 관한 블로깅 https://tutorialing.tistory.com/771
# 에 정리해 두었다.
# class SignupForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'password']

# 올바른 User form 생성
class SignupForm(UserCreationForm):
    # 이것은 "조건"에 대한 오버라이딩이다. 필수유무
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    # 이것은 "필드"에 대한 오버라이딩이다. "무엇"이 노출되길 원하는가에 따른 목록
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    # 이 함수 자체가 하나의 중복 이메일 가입을 방지하기 위한 기능이다.
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            qs = User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError('이미 등록된 이메일 주소 입니다.')
        return email