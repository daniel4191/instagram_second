from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import (
    LoginView, logout_then_login, 
    PasswordChangeView as AuthPasswordChangeView
    )
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .forms import SignupForm, ProfileForm, PasswordChangeForm
from .models import User

# Create your views here.
login = LoginView.as_view(
    template_name = 'accounts/login_form.html'
)

def logout(request):
    messages.success(request, '로그아웃 되었습니다.')
    return logout_then_login(request)

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            signed_user = form.save()

            # 이것으로 인해서 회원가입하자마자 로그인되는 기능
            auth_login(request, signed_user)
            messages.success(request, '회원가입 환영합니다.')
            # send_welcome_email은 forms.py의 User로 부터 비롯되었다.
            signed_user.send_welcome_email() # FIXME: Celery로 처리하는 것을 추천

            # root로 reverse url을 사용해줄때, 로그아웃 상태로 홈에 가게 되면
            # url의 가장 끝 인자로 next가 오게된다.
            # http://127.0.0.1:8000/accounts/login/?next=/
            # 이런식으로.
            # 때문에 이것을 해소하기 위한 조건문을 설정한다.
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
    else:
        form = SignupForm()
    return render(request, 'accounts/signup_form.html', {
        'form': form
    })

@login_required
def profile_edit(request):
    if request.method == 'POST':
        # ProfileForm은 기본적으로 ModelForm을 상속받았기 때문에 ()을 공백으로 두게 되면
        # 새로운 것을 생성하려고 시도할 것이기 때문에 instance를 지정해주어야 한다고 한다.
        form = ProfileForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, '프로필을 수정/저장 했습니다.')            
            return redirect('accounts:profile_edit')

    else:        
        form = ProfileForm(instance=request.user)

    return render(request, 'accounts/profile_edit_form.html', {
        'form': form
    })


class PasswordChangeView(LoginRequiredMixin, AuthPasswordChangeView):
    success_url = reverse_lazy('password_change')
    template_name = 'accounts/password_change_form.html'
    form_class = PasswordChangeForm

    def form_valid(self, form):
        messages.success(self.request, '암호를 변경 했습니다.')
        return super().form_valid(form)

password_change = PasswordChangeView.as_view()

# profile random picture
def profile_random(request):
    user = SignupForm
    return render(request, 'layout.html', {
        'user': user
    })


@login_required
def user_follow(request, username):    
    follow_user = get_object_or_404(User, username = username, is_active=True)
    
    # request.user => follow_user를 팔로우 하려고 합니다.    
    request.user.following_set.add(follow_user)
    follow_user.follower_set.add(request.user)

    messages.success(request, f'{follow_user}님을 팔로우 했습니다.')
    # 인자로 받게된 root는 가장 메인페이지로써, 프로젝트 단위 urls.py에 정의됨
    redirect_url = request.META.get('HTTP_REFERER', 'root')
    return redirect(redirect_url)


@login_required
def user_unfollow(request, username):
    unfollow_user = get_object_or_404(User, username = username, is_active=True)
    request.user.following_set.remove(unfollow_user)
    unfollow_user.follower_set.remove(request.user)
    messages.success(request, f'{unfollow_user}님을 언팔 했습니다.')
    redirect_url = request.META.get('HTTP_REFERER', 'root')
    return redirect(redirect_url)