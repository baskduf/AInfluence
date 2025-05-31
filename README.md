AI 자동 라이프스타일 블로그 포스팅 시스템
개요
이 프로젝트는 AI가 자동으로 여러 라이프스타일 관련 토픽을 생성하여 개인 블로그에 자동으로 일상을 포스팅하는 Django 기반 시스템입니다.
OpenAI의 ChatGPT API를 활용하여 자연스러운 포스트 내용을 생성하고, 30분마다 스케줄러를 통해 자동으로 게시됩니다.

주요 기능
AI 포스트 생성

ai_service 앱의 generate_post 함수가 OpenAI ChatGPT API에 프롬프트를 보내고, 응답으로 포스트 내용을 생성합니다.

프롬프트는 ai_service/prompt.txt에 정의되어 있습니다.

자동 포스팅

ai_post 앱의 auto_generate_post 함수가 /ai_post/post/ 경로로 요청을 받아, 내부적으로 /ai_service/generate_post/ API를 호출하여 AI가 생성한 내용을 자동으로 게시합니다.

30분마다 ai_post/scheduler.py에 정의된 스케줄러가 실행되어 자동 포스팅 작업을 수행합니다.

블로그 CRUD 기능

블로그 게시글의 생성, 조회, 수정, 삭제 기능은 board 앱에서 구현되어 있습니다.

주요 URL 경로:

pgsql
복사
편집
rewrite_process/
rewrite/
delete/
view/
write_process/
write/
기본 블로그 메인 페이지는 / 경로에서 확인할 수 있습니다.

디렉토리 구조 (주요 파일)
bash
복사
편집
ai_service/
 ├─ views.py           # OpenAI API 호출 및 포스트 생성 로직
 ├─ prompt.txt         # AI 프롬프트 템플릿

ai_post/
 ├─ views.py           # 자동 포스트 트리거 함수 (auto_generate_post)
 ├─ scheduler.py       # 30분마다 실행되는 스케줄러

board/
 ├─ views.py           # 블로그 CRUD 기능
 ├─ urls.py            # CRUD 관련 URL 패턴 정의
설치 및 실행
환경설정

Python 3.x, Django 최신 버전 권장

OpenAI API 키 환경변수 설정 필요 (OPENAI_API_KEY)

의존성 설치

bash
복사
편집
pip install -r requirements.txt
마이그레이션 및 서버 실행

bash
복사
편집
python manage.py migrate
python manage.py runserver
스케줄러 실행

ai_post/scheduler.py 내 스케줄러가 30분마다 auto_generate_post를 호출하도록 설정되어 있습니다.

스케줄러 실행 방법은 프로젝트 설정에 따라 다를 수 있으므로 (예: cron, celery beat 등) 환경에 맞게 적용하세요.

API 엔드포인트
AI 포스트 생성
POST /ai_service/generate_post/

OpenAI API 요청 후 포스트 내용을 반환.

자동 포스팅 트리거
POST /ai_post/post/

AI 포스트 생성 API를 호출 후, 게시글로 저장.

블로그 게시글 관련 (board 앱)

bash
복사
편집
GET/POST /write/            # 새 글 작성 페이지
POST /write_process/        # 새 글 작성 처리
GET/POST /rewrite/          # 글 수정 페이지
POST /rewrite_process/      # 글 수정 처리
POST /delete/               # 글 삭제 처리
GET /view/                  # 글 상세 조회
GET /                       # 블로그 메인 페이지 (글 목록)
참고사항
ai_service/prompt.txt 파일 내에 AI에게 전달할 프롬프트 문구를 자유롭게 수정하여 다양한 라이프스타일 주제의 글을 생성할 수 있습니다.

OpenAI API 호출 시 비용이 발생할 수 있으니, API 사용량에 주의하세요.

스케줄러 설정은 서버 환경에 맞게 조정해야 하며, 현재는 30분 간격으로 자동 실행됩니다.
