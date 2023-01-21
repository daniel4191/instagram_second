from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.contrib.auth.views import LoginView, logout_then_login
from django.contrib.auth.decorators import login_required

from .forms import SignupForm
# Create your views here.


# 기본 LoginView에서 커스터마이징이 필요하다면
# as_view()안의 인자를 model = Post 이런식으로 오버라이드 해줌으로 활용 가능하다.
login = LoginView.as_view(
    template_name='accounts/login_form.html'
)


def logout(request):
    # 이 메세지는 필수값은 아니다. 다만, 이 기능이 성공했을때 어떤 메세지를 노출해줄것인가에 대한 기능이다.
    messages.success(request, '로그아웃 되었습니다.')

    # 이 logout_then_login 내장 함수는
    # "로그아웃 하자마자 로그인페이지로 리다이렉트 시키겠다."라는 의미다.
    return logout_then_login(request)


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            signed_user = form.save()
            auth_login(request, signed_user)
            messages.success(request, '회원가입 환영합니다.')
            # 가입된 회원에게 이메일 발송 서비스
            signed_user.send_welcome_email()  # FIXME: Celery로 처리하는 것을 추천

            # 여기서 redirect의 인자로 받은 'root'는 프로젝트 단위의 urls.py에서 name으로 설정된 것이다.
            # return redirect('root')

            # login_required로 장식한 상태에서 비로그인 상태라면 page_not_found에러와 함께
            # next라는 인자가 url로 전달이 된다. 그것을 처리하기 위한 기능이다.
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
    else:
        form = SignupForm()
    return render(request, 'accounts/signup_form.html', {
        'form': form
    })


@login_required
def profile_edit(request):
    return render(request, 'accounts/profile_edit_form.html', {

    })
    pass
