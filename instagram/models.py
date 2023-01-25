from django.db import models
from django.conf import settings

import re

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='instagram/post/%Y/%m/%d')
    # max_length가 필요한 경우는 CharField, 필요없는 경우는 TextField를 써주면 된다.
    caption = models.CharField(max_length=500)
    tag_set = models.ManyToManyField('Tag', blank = True)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.caption

    def extract_tag_list(self):
        # #다음을 ()로 묶어 줘야, 결과값으로 #를 붙여주지 않고 리턴할 수 있다.
        tag_name_list = re.findall(r'#([a-zA-Z\dㄱ-힣]+)', self.caption)
        tag_list = []
        for tag_name in tag_name_list:
            tag, _ = Tag.objects.get_or_create(name = tag_name)
            tag_list.append(tag)

    # def get_absolute_url(self):
    #     return reverse('()', kwargs={'pk': self.pk})
    

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name