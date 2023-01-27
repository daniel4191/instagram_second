from django import template

register = template.Library()


'''
아래의 정의된 함수는
def cut(value, arg):
    return value.replace(arg, ')
에 대한 정의이다.

이렇게 정의해준 후에 html에서 탬플릿 태그로써 사용하게 된다면
{{ front|cut:'0' }}
이라고 될때, cut함수를 통해서 들어온 value값이 front로 가게되고 cut:뒤에 있는
'0'값이 arg로 가게 된다.
'''
@register.filter
def is_like_user(post, user):
    return post.is_like_user(user)