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


def sign_up(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            if password == confirm_password and (not User.objects.filter(username=username).exists()):
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                return redirect('/board')

    form = SignupForm()
    return render(request, template_name="sign_up.html", context={"form":form})
