import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json

@csrf_exempt
def generate_post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    data = json.loads(request.body)
    topic = data.get("topic", "여름 브런치 데이트")

    with open("ai_service/prompt.txt", "r", encoding="utf-8") as f:
        prompt_template = f.read()
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
