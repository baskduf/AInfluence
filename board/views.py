from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .models import Post
from .forms import WriteForm
from django.shortcuts import redirect

from django.shortcuts import render, redirect
from .models import Post
from .forms import WriteForm

def rewrite(request):
    if 'boardNo' in request.GET:
        if request.user.is_authenticated:
            post_id = request.GET['boardNo']
            post = Post.objects.filter(id=post_id).first()

            if post:
                # 작성자 본인이거나 관리자(superuser)인 경우만 수정 가능
                if post.author == request.user or request.user.is_superuser:
                    form = WriteForm(instance=post)  # 여기서 instance 사용
                    return render(request, 'rewrite_form.html', {'form': form, 'post_id': post.id})

    return render(request, 'login_error.html')


def rewrite_process(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = WriteForm(request.POST)
            post = Post.objects.filter(id=request.POST['id']).first()
            if post is not None:
                if post.author.username == request.user.username or request.user.is_superuser:
                    post.title = form.data['title']
                    post.content = form.data['content']
                    post.save()
                    return redirect('/board')

    return render(request, 'login_error.html')


def delete(request):
    if 'boardNo' in request.GET:
        id = request.GET['boardNo']
        post = Post.objects.filter(id=id)
        if request.user.is_authenticated:
            if request.user.is_superuser or (post.filter(author=request.user) is not None):
                post.delete()
                return redirect('/board')
    return render(request, 'login_error.html')

def write(request):
    if request.user.is_authenticated:
        post = WriteForm()
        return render(request, 'write_form.html', {'form': post})
    else:
        return render(request, 'login_error.html')


def write_process(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = WriteForm(request.POST)
            if form.is_valid():
                post = Post()
                post.title = form.cleaned_data['title']
                post.content = form.cleaned_data['content']
                post.author = request.user
                post.save()
                return redirect('/board')

    return render(request, 'login_error.html')

def view_post(request):
    form = AuthenticationForm(request.user)
    if 'boardNo' in request.GET:
        post = Post.objects.filter(id=request.GET['boardNo']).first()
        if post is not None:
            return render(request, 'view_form.html', {'form':form, 'post': post})

    return render(request, 'login_error.html')

from django.core.paginator import Paginator

def index(request):
    form = AuthenticationForm()
    posts_list = Post.objects.all().order_by('-created_at')  # 최신순 정렬 추천

    paginator = Paginator(posts_list, 10)  # 한 페이지에 10개씩 보여주기
    page_number = request.GET.get('page', 1)  # URL 파라미터 ?page=1 기본값 1
    page_obj = paginator.get_page(page_number)  # 페이지 객체

    
    return render(request, 'index.html', {'form': form, 'page_obj': page_obj})
