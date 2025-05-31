import random
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from board.models import Post  # board 앱의 게시글 모델 import

User = get_user_model()

TOPIC_LIST = [
    "여름 브런치 데이트",
    "비 오는 날 감성",
    "혼자만의 여행",
    "카페에서의 하루",
    "따뜻한 아침 루틴",
    "봄꽃 산책 코스 추천",
    "책과 함께하는 조용한 오후",
    "도시 속 숨은 맛집 탐방",
    "소소한 다이어트 레시피",
    "감성적인 밤 산책",
    "내추럴 뷰티 루틴 공유",
    "주말에 가고 싶은 전시회",
    "취미로 시작하는 일러스트 그리기",
    "요가와 명상으로 힐링하기",
    "계절별 패션 스타일링 팁",
    "셀프 케어 루틴 공개",
    "작은 카페 인테리어 아이디어",
    "인생 첫 해외여행 준비기",
    "친구와 떠난 당일치기 여행",
    "마음에 드는 음악 플레이리스트",
    "새벽 감성 일기 쓰기",
    "손편지 쓰기의 따뜻함",
    "내 방 꾸미기 소소한 팁",
    "자연과 함께하는 캠핑 이야기",
    "겨울철 건강 관리 방법",
    "감성 가득한 영화 추천",
    "나만의 플래너 꾸미기",
    "달콤한 홈 베이킹 도전기",
    "비건 요리 쉽게 시작하기",
    "힐링이 필요한 날의 음악",
    "따뜻한 차와 함께하는 오후",
    "가벼운 러닝으로 하루 시작하기",
    "소중한 사람에게 보내는 메시지",
    "새로운 취미, 사진 찍기",
    "작가가 추천하는 에세이 모음",
    "편안한 홈카페 만들기",
    "소확행, 작은 행복 찾기",
    "가을 단풍 여행지 추천",
    "마음 챙김 명상 팁",
    "감성 가득한 플라워 클래스",
]


@csrf_exempt
def auto_generate_post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST 요청만 허용됨"}, status=405)

    topic = random.choice(TOPIC_LIST)

    try:
        response = requests.post(
            "http://localhost:8000/ai_service/generate_post/",  # URL은 실제 배포 환경에 맞게 변경
            json={"topic": topic},
            timeout=500
        )
        if response.status_code != 200:
            return JsonResponse({"error": "generate_post API 호출 실패", "status": response.status_code}, status=500)

        data = response.json()
        title = data.get("title", "")
        content = data.get("content", "")
        image_url = data.get("image_url", "")

        # 자동 포스팅용 유저
        ai_user = User.objects.filter(username="root").first()
        if not ai_user:
            return JsonResponse({"error": "'aibot' 유저가 존재하지 않습니다."}, status=500)

        # 이미지 저장은 URL이므로 별도 다운로드 및 저장 생략 (필요시 구현 가능)
        post = Post.objects.create(
            title=title,
            content=content,
            author=ai_user,
        )

        # 이미지가 있을 경우 필드에 저장 (단순 URL 링크만 표시할 경우에는 생략 가능)
        if image_url:
            import urllib.request
            from django.core.files.base import ContentFile
            import os

            result = urllib.request.urlretrieve(image_url)
            with open(result[0], 'rb') as f:
                post.image.save(
                    f"{post.id}_image.png",
                    ContentFile(f.read()),
                    save=True
                )

        return JsonResponse({"message": "게시글 자동 생성 완료", "topic": topic})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
