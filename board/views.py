from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .models import Post
from .forms import WriteForm
from django.shortcuts import redirect

def rewrite(request):
    if 'boardNo' in request.GET:
        if request.user.is_authenticated:
            id = request.GET['boardNo'];
            post_id = Post.objects.filter(id=id).first()
            if post_id is not None:
                if post_id.author.username == request.user.username or request.user.is_superuser:
                    form = WriteForm()
                    form.id = post_id.id
                    form.title = post_id.title
                    form.content = post_id.content
                    form.save()
                    return render(request, 'rewrite_form.html', {'form': form})
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

def index(request):
    form = AuthenticationForm()
    posts = Post.objects.all()
    return render(request, 'index.html', {'form': form, 'posts': posts})
