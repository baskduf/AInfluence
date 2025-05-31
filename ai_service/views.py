import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import requests

@csrf_exempt
def generate_post(request):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)
        
        import json
        data = json.loads(request.body)
        topic = data.get("topic", "여름 브런치 데이트")
        
        # prompt.txt 읽기
        with open("ai_service/prompt.txt", "r", encoding="utf-8") as f:
            prompt_template = f.read()
        prompt = prompt_template.replace("{topic}", topic)
        
        # ChatGPT 호출
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            api_key=settings.OPENAI_API_KEY,
        )
        content = response.choices[0].message['content']
        
        # 파싱
        def get_section(text, label):
            start = text.find(label) + len(label)
            end = text.find("\n", start)
            if end == -1:
                end = len(text)
            return text[start:end].strip()
        
        title = get_section(content, "제목:")
        content_start = content.find("내용:") + len("내용:")
        image_start = content.find("이미지:")
        body = content[content_start:image_start].strip()
        image_prompt = content[image_start + len("이미지:"):].strip()
        
        # 이미지 생성 (DALL·E)
        image_response = openai.Image.create(
            prompt=image_prompt,
            n=1,
            size="512x512",
            api_key=settings.OPENAI_API_KEY,
        )
        image_url = image_response['data'][0]['url']
        
        # JSON으로 결과 반환 (이미지는 URL로)
        return JsonResponse({
            "title": title,
            "content": body,
            "image_url": image_url,
        })
    else:
        return JsonResponse({"error": "POST method required"}, status=405)
