from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from .forms import PostForm, CommentForm
from .models import Tag, Post

# Create your views here.
@login_required
def index(request):
    # 지금시간으로부터 3일의 시간을 뺀다는 소리
    timesince = timezone.now() - timedelta(days=3)
    # filter 안의 인자의 뜻은 이러하다
    # author(작성자)가 포함이 되어있는가? = 여기에
    # post_list = Post.objects.all().filter(author__in = request.user.following_set.all())

    # post_list 구현 두번째 방법
    # 작성자가 자기 자신이거나
    # 작성자가 following 목록에 들어있는가.
    post_list = Post.objects.all().filter(
        Q(author=request.user) |  Q(author__in=request.user.following_set.all())
        ).filter(
            created_at__gte = timesince
        )
    # 이렇게 정의해주고 싶을때, 여기는 instagram앱 안이고, User 모델은 accounts 앱 안에 정의 되어있다.
    # User.objects.all()
    
    # 때문에 accounts의 User를 import로 받아오는 것 보다는
    # from django.contrib.auth import get_user_model
    # 을 사용하는 것이 유연한 방법이다.

    # exclude를 써줄때는 objects.all()로 앞에 붙여주나 objects만 있거나 똑같다.
    # suggested_user_list = get_user_model().objects.all().exclude()
    suggested_user_list = get_user_model().objects.exclude(pk = request.user.pk)\
        .exclude(pk__in = request.user.following_set.all())[:3]

    # form 전송을 위한 정의
    comment_form = CommentForm()

    return render(request, 'instagram/index.html', {
        'post_list': post_list,
        'suggested_user_list': suggested_user_list,
        'comment_form': comment_form
    })
    



@login_required
def post_new(request):
    if request.method == 'POST':
        
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # 모델에 대한 필수필드 지정없이 save를 하게 되면 "인티그리티"에러가 발생한다고 한다.
            # 때문에 commit을 False로 해주었다.
            post = form.save(commit=False)
            post.author = request.user              
            post.save()
            post.tag_set.add(*post.extract_tag_list())          
            messages.success(request, '포스팅을 저장했습니다.')
            # get_absolute_url을 models.py에서 지정해준 후에 여기의 인자로 넣어줬음.
            # get_absolute_url를 설정하게 되면 해당 get_absolute_url로 지정된 위치로 이동됨
            
            return redirect(post)

    else:
        form = PostForm()

    return render(request, 'instagram/post_form.html', {
        'form': form   
    })

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment_form = CommentForm()
    return render(request, 'instagram/post_detail.html', {
        'post': post,
        'comment_form': comment_form
    })


@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.add(request.user)
    messages.success(request, f'포스팅#{post.pk}를 좋아합니다.')
    redirect_url = request.META.get('HTTP_REFERER', 'root')
    return redirect(redirect_url)


@login_required
def post_unlike(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.remove(request.user)
    messages.success(request, f'포스팅#{post.pk}를 취소합니다. ')
    redirect_url = request.META.get('HTTP_REFERER', 'root')
    return redirect(redirect_url)


def user_page(request, username):
    page_user = get_object_or_404(get_user_model(), username = username, is_active = True)
    # is_active는 "허용된 사람만 보겠다."라는 의미다.
    page_user = get_object_or_404(get_user_model(), username = username, is_active=True)
    post_list = Post.objects.filter(author = page_user)
    post_list_count = post_list.count() # 실제 데이터베이스에 count 쿼리를 던지게 됩니다.
    
    # request.user는 기본적으로 "로그인시" User 객체가 되는거고, "비 로그인 시" AnonymousUser가 된다.
    if request.user.is_authenticated:
        is_follow = request.user.following_set.filter(pk = page_user.pk).exists()
    else:
        is_follow = False

    return render(request, 'instagram/user_page.html', {
        'page_user': page_user,
        'post_list': post_list,
        'post_list_count': post_list_count,
        'is_follow': is_follow
    })


@login_required
def comment_new(request, post_pk):
    post = get_object_or_404(Post, pk = post_pk)

    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return render(request, 'instagram/_comment.html', {
                    'comment': comment
                })
            return redirect(comment.post)
            
    else:
        form = CommentForm()
    return render(request, 'instagram/comment_form.html', {
        'form': form
    })