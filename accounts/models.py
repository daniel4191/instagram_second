from django.conf import settings
# from ..askcompany.settings import common
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string

# Create your models here.
class User(AbstractUser):
    website_url = models.URLField(blank = True)
    bio = models.TextField(blank = True)

    def send_welcome_email(self):
        subject = render_to_string('accounts/welcome_email_subject.txt', {
            'user': self
        })
        content = render_to_string('accounts/welcome_email_content.txt',{
            'user': self
        })

        # 여기서 settings는 django.conf라는 곳에서 임포트 해오는 것이고
        # 기초 settings.py의 이름이 변하더라도 거기서 가져오는 것 같다.
        # 문제 생길 시, 추측이 아닐 수 있으니 settings를 common으로 변경해주자.
        sender_email = settings.WELCOME_EMAIL_SENDER
        # 여기서 self.email의 의미는 User마다 email로 가입이 될텐데, 그 주소가 수신주소가 되는것이다.
        send_mail(subject, content, sender_email, [self.email], fail_silently=False)

    # save할때마다 호출 -> which mean is User가 생성될때마다
    # 이런식의 로직 구현이 가능하다.
    def save(self, *args, **kwargs):
        is_created = (self.pk == None)
        super().save(*args, **kwargs)

        if is_created:
            pass