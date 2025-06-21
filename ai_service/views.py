import json
import threading
import requests
import urllib.request
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from django.conf import settings
import openai

from board.models import Post, Comment

@csrf_exempt
def generate_post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    data = json.loads(request.body)
    topic = data.get("topic", "여름 브런치 데이트")
    post_id = data.get("post_id")

    with open("ai_service/prompt.txt", "r", encoding="utf-8") as f:
        prompt_template = f.read()

    feedback_text = ""
    if post_id:
        from board.models import Comment
        comments = Comment.objects.filter(post_id=post_id).order_by('-created_at')[:5]
        if comments:
            feedback_text = "\n\n# 사용자 피드백:\n" + "\n".join(f"- {c.content}" for c in comments)

    prompt = prompt_template.replace("{topic}", topic)

    openai.api_key = settings.OPENAI_API_KEY

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
    )
    content = response.choices[0].message.content

    def get_section(text, label, next_label=None):
        start = text.find(label)
        if start == -1:
            return ""
        start += len(label)
        if next_label:
            end = text.find(next_label, start)
            if end == -1:
                end = len(text)
        else:
            end = len(text)
        return text[start:end].strip()

    title = get_section(content, "제목:", "내용:")
    body = get_section(content, "내용:", "이미지:")
    image_prompt = get_section(content, "이미지:")

    # 이미지 생성
    image_response = openai.images.generate(
        prompt=image_prompt,
        n=1,
        size="512x512",
    )
    image_url = image_response.data[0].url

    return JsonResponse({
        "title": title,
        "content": body,
        "image_url": image_url,
    })

def generate_gpt_post_background(post):
    def task():
        print("[ai_service] ✅ GPT 백그라운드 task 시작")  # <== 시작 로그

        try:
            with open("ai_service/prompt.txt", "r", encoding="utf-8") as f:
                prompt_template = f.read()

            recent_comments = Comment.objects.filter(post_id=post.id).order_by('-created_at')[:5]
            feedback_text = ""
            if recent_comments:
                feedback_text = "\n\n# 사용자 피드백:\n" + "\n".join(f"- {c.content}" for c in recent_comments)

            prompt = prompt_template.replace("{topic}", post.title) + feedback_text
            openai.api_key = settings.OPENAI_API_KEY

            print("[ai_service] 📝 GPT 요청 프롬프트 준비 완료")

            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
            )
            content = response.choices[0].message.content
            print("[ai_service] 🧠 GPT 응답 수신 완료")

            def get_section(text, label, next_label=None):
                start = text.find(label)
                if start == -1:
                    print(f"[ai_service] ⚠ '{label}' 구간 없음")
                    return ""
                start += len(label)
                end = text.find(next_label, start) if next_label else len(text)
                if end == -1:
                    end = len(text)
                return text[start:end].strip()

            title = get_section(content, "제목:", "내용:")
            body = get_section(content, "내용:", "이미지:")
            image_prompt = get_section(content, "이미지:")

            print(f"[ai_service] 📄 추출된 제목: {title}")
            print(f"[ai_service] 📄 추출된 이미지 프롬프트: {image_prompt}")

            image_response = openai.images.generate(prompt=image_prompt, n=1, size="512x512")
            image_url = image_response.data[0].url
            print("[ai_service] 🖼 이미지 생성 완료")

            ai_user = User.objects.filter(username="ai_influencer").first()
            if not ai_user:
                ai_user = User.objects.create_user(username="ai_influencer", password="ai_influencer")
                print("[ai_service] 👤 ai_influencer 계정 생성됨")

            new_post = Post.objects.create(
                title=title or "제목 없음",
                content=body or "내용 없음",
                author=ai_user,
                origin_post=post
            )

            result = urllib.request.urlretrieve(image_url)
            with open(result[0], 'rb') as f:
                new_post.image.save(
                    f"{new_post.id}_image.png",
                    ContentFile(f.read()),
                    save=True
                )

            print(f"[ai_service] ✅ 최종 글 생성 완료: {new_post.title}")

        except Exception as e:
            print("[ai_service] ❌ GPT 생성 중 예외 발생:", str(e))

    threading.Thread(target=task).start()



@csrf_exempt
def trigger_generate(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        data = json.loads(request.body)
        post_id = data.get("post_id")
        post = Post.objects.filter(id=post_id).first()

        if not post:
            return JsonResponse({"error": "Post not found"}, status=404)

        # 중복 생성 방지
        already_generated = Post.objects.filter(origin_post=post).exists()
        if already_generated:
            return JsonResponse({"message": "Already generated"}, status=200)

        # 댓글 수 3개 이상이어야 함
        if post.comments.count() < 3:
            return JsonResponse({"message": "Not enough comments"}, status=200)

        generate_gpt_post_background(post)
        return JsonResponse({"message": "GPT 생성 시작됨"}, status=202)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)