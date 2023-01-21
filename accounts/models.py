from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

# Create your models here.
# User model은 account(계정)생성에 있어서 가장 기초가 되는 필수요소이다.
# 그리고 그런 필수 요소인 User를 세팅하는 내부 기능은 모두 from django.contrib.auth.models import AbstractUser
# 으로부터 상속받아서 쓸 수 있다. (User한정느낌_불확실)

# settings에 AUTH_USER_MODEL 정의 필요


class User(AbstractUser):
    website_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)

    # 이거는 재정의 해줄때 사용하는 것이다. (오버라이드)
    # def save(self, *args, **kwargs):
    #     is_created = (self.pk == None)
    #     super().save(*args, **kwargs)

    def send_welcome_email(self):
        # 템플릿을 이용해서 문자열을 생성할때 사용하는 것 render_to_string()
        subject = render_to_string('accounts/welcome_email_subject.txt', {
            'user': self
        })
        content = render_to_string('accounts/welcome_email_content.txt', {
            'user': self
        })
        # 이것도 BASE_DIR을 기준으로 askcompany.settings.common으로 가게 될줄 알았는데
        # settings를 import 해서 처리했다.
        sender_email = settings.WELCOME_EMAIL_SENDER
        # 현재 이 send_mail은 send_welcome_email이라는 함수 안에 들어있는 것이며
        # send_welcome_email함수는 User라는 클래스 안에 귀속이 되어있는 것이다.
        # 여기서 말하는 self.email은 해당 User에 귀속되어진 이메일이다.
        return send_mail(subject, content, sender_email, [
            self.email], fail_silently=False)
