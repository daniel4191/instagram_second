from django.urls import path, re_path
from django.contrib.auth.validators import UnicodeUsernameValidator

from . import views

app_name = 'instagram'

username_regex = UnicodeUsernameValidator.regex.lstrip('^').strip('$')

# 바로 위에 정의해준 username_regex가 계속 에러가 나기때문에 어떤 내용으로 출력이 되는지 확인하고자 한 코드
# 이 repr은 무엇을 표현할때 쓰는 걸까?
print('username_regex :', repr(username_regex))

urlpatterns = [
    path('', views.index, name = 'index'),
    path('post/new/', views.post_new, name = 'post_new'),
    path('post/<int:pk>/', views.post_detail, name = 'post_detail'),
    # path(r'(?P<username>'+ UnicodeUsernameValidator.regex +')/', views.user_page, name = 'user_page')
    # re_path(r'^(?P<username>'+ username_regex +')/', views.user_page, name = 'user_page')
    re_path(r'^(?P<username>[\w.@+-]+)/$', views.user_page, name = 'user_page')
]
