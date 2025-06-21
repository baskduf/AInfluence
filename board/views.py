from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .models import Post
from .forms import WriteForm
from django.shortcuts import redirect
from .models import Post, Comment
from .forms import CommentForm

from django.shortcuts import render, redirect
from .models import Post
from .forms import WriteForm

def view_post(request):
    form = AuthenticationForm(request.user)
    comment_form = CommentForm()

    if 'boardNo' in request.GET:
        post = Post.objects.filter(id=request.GET['boardNo']).first()
        if post is None:
            return render(request, 'login_error.html')

        if request.method == 'POST' and request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()

                # ✅ 댓글 수 확인
                total_comments = post.comments.count()

                if total_comments >= 3:
                    # 중복 생성은 ai_service에서 처리
                    import requests
                    try:
                        requests.post(
                            "http://localhost:8000/ai_service/trigger_generate/",
                            json={"post_id": post.id},
                            timeout=3  # 응답 기다리지 않음
                        )
                        print("[board] GPT 트리거 요청 전송 완료")
                    except Exception as e:
                        print("[board] GPT 트리거 요청 실패:", str(e))

                return redirect(f'/view?boardNo={post.id}')

        comments = post.comments.all().order_by('-created_at')
        return render(request, 'view_form.html', {
            'form': form,
            'post': post,
            'comment_form': comment_form,
            'comments': comments,
        })

    return render(request, 'login_error.html')
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

from django.core.paginator import Paginator

def index(request):
    form = AuthenticationForm()
    posts_list = Post.objects.all().order_by('-created_at')  # 최신순 정렬 추천

    paginator = Paginator(posts_list, 10)  # 한 페이지에 10개씩 보여주기
    page_number = request.GET.get('page', 1)  # URL 파라미터 ?page=1 기본값 1
    page_obj = paginator.get_page(page_number)  # 페이지 객체

    
    return render(request, 'index.html', {'form': form, 'page_obj': page_obj})

def delete_comment(request, comment_id):
    comment = Comment.objects.filter(id=comment_id).first()
    if comment and request.user == comment.author:
        comment.delete()
        return redirect(f'/view?boardNo={comment.post.id}')
    return render(request, 'login_error.html')
