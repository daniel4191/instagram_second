from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
# User model은 account(계정)생성에 있어서 가장 기초가 되는 필수요소이다.
# 그리고 그런 필수 요소인 User를 세팅하는 내부 기능은 모두 from django.contrib.auth.models import AbstractUser
# 으로부터 상속받아서 쓸 수 있다. (User한정느낌_불확실)

# settings에 AUTH_USER_MODEL 정의 필요


class User(AbstractUser):
    website_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
