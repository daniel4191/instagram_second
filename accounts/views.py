from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import SignupForm
# Create your views here.


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, '회원가입 환영합니다.')
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
