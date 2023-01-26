from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import PostForm
from .models import Tag, Post

# Create your views here.
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
    return render(request, 'instagram/post_detail.html', {
        'post': post
    })