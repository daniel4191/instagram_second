from django.db import models
from django.conf import settings
from django.urls import reverse

import re

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # 이것을 지정해 주는 것으로, DB 테이블은 만들어 지지 않는다.
        # 이 BaseModel 클래스는 "부모 클래스"로써 남아 있기위해 만드는 것이기 때문이다.
        abstract = True

# class Post(models.Model):

# user 정보를 획득할 때 몇가지 방법이 있지만
# 방법1 -> Post.objects.filter(author=user)
# 라는 방식으로 SQL 형태로 얻을 수도 있고

# 방법2 -> user.post_set.all()
# 라는 형태로 얻을 수도 있다.(이것도 SQL 형식이긴 한데 다름 구체적으로는 아직 잘 모르겠음)
# 정확히는 post_set이라는 것은 post라는 이름을 가진 클래스 하에서 자동생성 된다는 것은 알고 있는데
# post라는 이름의 클래스 하에 있으면서, settings.AUTH_USER_MODEL이라는 것을 상속받은 개체만 클래스명_set이라고
# 자동생성 되는 것일까? 아직은 명확히 모르겠다.

class Post(BaseModel):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='my_post_set')
    photo = models.ImageField(upload_to='instagram/post/%Y/%m/%d')
    # max_length가 필요한 경우는 CharField, 필요없는 경우는 TextField를 써주면 된다.
    caption = models.CharField(max_length=500)
    tag_set = models.ManyToManyField('Tag', blank = True)
    location = models.CharField(max_length=100)    
    # ManyToManyField 정의법 1 - 기존 포스트에 추가하기
    like_user_set = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank = True, related_name='like_post_set')

    # instagram.Post.author와 instagram.Post.like_user_set의 Reverse accessor 'User.post_set'
    # 가 서로 충돌이 일어난다. 라는 말이다.
    # 이것의 원인으로는 현재 author와 like_user_set은 settings.AUTH_USER_MODEL을 받아와 사용하고 있다.
    # 따라서 related_name이 자동적으로 class의 이름을 따라서 "post_set"이 되는데,
    # 둘 중 하나의 related_name을 변경해주면 해결되는 문제다.
    # 혹은 둘중 하나의 related_name을 '+'로 써주면 그거는 포기하겠다. 라는 뜻이라는데
    # 애초에 related_name은 왜 필요한걸까?
    
    # related_name은 ORM 패턴을 위해서 쓰는 것이고 ForeignKey의 개념으로써 "무언가를 참조한다."라는
    # 의미로 이해하면 될것같다.
    # 혹은 그 내 자신이 A일때, B가 A를 참조하고 싶을때 사용하는 일종의 "주소"개념인것같다. 
    """
    ERRORS:
instagram.Post.author: (fields.E304) Reverse accessor 'User.post_set' for 'instagram.Post.author' clashes with reverse accessor for 'instagram.Post.like_user_set'.
        HINT: Add or change a related_name argument to the definition for 'instagram.Post.author' or 'instagram.Post.like_user_set'.
instagram.Post.like_user_set: (fields.E304) Reverse accessor 'User.post_set' for 'instagram.Post.like_user_set' clashes with reverse accessor for 'instagram.Post.author'.
        HINT: Add or change a related_name argument to the definition for 'instagram.Post.like_user_set' or 'instagram.Post.author'.
    """

    def __str__(self):
        return self.caption

    @property
    def author_name(self):
        return f'{self.author.first_name} {self.author.last_name}'

    def extract_tag_list(self):
        # #다음을 ()로 묶어 줘야, 결과값으로 #를 붙여주지 않고 리턴할 수 있다.
        tag_name_list = re.findall(r'#([a-zA-Z\dㄱ-힣]+)', self.caption)
        tag_list = []
        for tag_name in tag_name_list:
            tag, _ = Tag.objects.get_or_create(name = tag_name)
            tag_list.append(tag)
        return tag_list

    def get_absolute_url(self):
        # 방법1
        # return reverse('()', kwargs={'pk': self.pk})

        # 방법2
        return reverse('instagram:post_detail', args=[self.pk])

    def is_like_user(self, user):
        return self.like_user_set.filter(pk=user.pk).exists()

    class Meta:
        ordering = ['-pk']
    

class Comment(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    message = models.TextField()

    class Meta:
        ordering = ['-id']


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# ManyToManyField 정의법 2 - 클래스 생성하기
# ManyToManyField 정의법 3 - 이 클래스를 ManyToManyField에 오버라이딩 형식으로 커스텀해서 사용한다.
# class LikeUser(models.Model):
#     post = models.ForeignKey(Post, on_delete= models.CASCADE)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)