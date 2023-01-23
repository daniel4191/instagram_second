from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, logout_then_login
from django.contrib.auth import login as auth_login

from .forms import SignupForm


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
            signed_user.send_welcome_email()            

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