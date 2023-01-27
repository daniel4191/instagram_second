from django.conf import settings
# from ..askcompany.settings import common
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail, BadHeaderError
from django.db import models
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.core.validators import RegexValidator
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.shortcuts import resolve_url

# Create your models here.
class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = 'M', '남성'
        FEMALE = 'F', '여성'

    # 기본적으로 ManyToManyField는 처음에 "대상"을 정해줘야한다.
    # 그런데 이 User 모델 하에서는 자기 자신이 된다는 의미로 self로 해준다고 하는데, 이건 잘 모르겠다.
    
    # 뒤 이어 나온 blank를 True로 해주는 이유는 "팔로워나 팔로잉이 없을 수 도 있으니까"가 이유다.
    follower_set = models.ManyToManyField("self", blank=True)    
    following_set = models.ManyToManyField("self", blank=True)
    
    website_url = models.URLField(blank = True)
    bio = models.TextField(blank = True)
    # 이게 max_length가 13인 이유는 휴대폰번호 기본 11자리(3+4+4)와 -가 2번나오기 때문이다.
    phone_number = models.CharField(max_length = 13, blank=True, validators=[RegexValidator(r'^010[1-9]\d{3}-?\d{4}$')])    
    gender = models.CharField(max_length = 1, blank=True, choices = GenderChoices.choices)
    profile = models.ImageField(blank=True, upload_to='accounts/profile/%Y/%m/%d')
    avatar = models.ImageField(blank = True, upload_to='accounts/avatart/%Y/%m/%d',
        # 이 help_text는 안내 문구다.
        help_text = '48px * 48px 크기의 png/jpg 파일을 업로드 해주세요.')
    # source는 "어떤 인스턴스를 대상으로해서 변환을 할지"
    # processors는 어떤 과정을 거치고
    # format은 어떤 포멧으로 세팅을하고    
    # 참조: https://github.com/matthewwithanm/django-imagekit
    avatar_thumbnail = ImageSpecField(source='avatar',
                                      processors=[ResizeToFill(100, 50)],
                                      format='JPEG',
                                      options={'quality': 60})
        
    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return resolve_url('pydenticon_image', self.username)

    def send_welcome_email(self):
        subject = render_to_string('accounts/welcome_email_subject.txt', {
            'user': self
        })
        subject

        content = render_to_string('accounts/welcome_email_content.txt',{
            'user': self
        })
        content

        # 여기서 settings는 django.conf라는 곳에서 임포트 해오는 것이고
        # 기초 settings.py의 이름이 변하더라도 거기서 가져오는 것 같다.
        # 문제 생길 시, 추측이 아닐 수 있으니 settings를 common으로 변경해주자.
        sender_email = settings.WELCOME_EMAIL_SENDER
        sender_email

        if subject and content and sender_email:
            try:
                # 여기서 self.email의 의미는 User마다 email로 가입이 될텐데, 그 주소가 수신주소가 되는것이다.
                send_mail(subject, content, sender_email, [self.email], fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid Header found.')
            return HttpResponseRedirect('/')
        else:
            # In reality we'd use a form class
            # to get proper validation errors.
            return HttpResponse('Make sure all fields are entered and valid.')

    # save할때마다 호출 -> which mean is User가 생성될때마다
    # 이런식의 로직 구현이 가능하다.
    def save(self, *args, **kwargs):
        is_created = (self.pk == None)
        super().save(*args, **kwargs)

        if is_created:
            pass