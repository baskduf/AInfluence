from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .forms import SignupForm

# Create your views here.

def logout_controller(request):
    if request.user.is_authenticated:
        h = logout(request)
        return redirect('/board')
    else:
        return render(request, 'login_error.html')

def login_controller(request):
    if request.method == 'GET':
        return render(request, 'login_error.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        authenticated = authenticate(request, username=username, password=password)
        if authenticated is not None:
            login(request, authenticated)
            return redirect('/board')
        else:
            return render(request, 'login_error.html')


from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import SignupForm  # 폼 import

def sign_up(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # username 중복 체크는 form 내부 clean_username()에서 이미 함
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('/board')

        # 유효성 검사 실패 → form 그대로 넘겨줘야 오류 메시지가 출력됨
        return render(request, 'sign_up.html', {'form': form})

    else:
        form = SignupForm()
        return render(request, 'sign_up.html', {'form': form})
