# AI 자동 라이프스타일 블로그 포스팅 시스템

## 개요  
이 프로젝트는 AI가 자동으로 여러 라이프스타일 관련 토픽을 생성하여 개인 블로그에 자동으로 일상을 포스팅하는 Django 기반 시스템입니다.  
OpenAI의 ChatGPT API를 활용하여 자연스러운 포스트 내용을 생성하고, 30분마다 스케줄러를 통해 자동으로 게시됩니다.

---

## 주요 기능

- **AI 포스트 생성**  
  - `ai_service` 앱의 `generate_post` 함수가 OpenAI ChatGPT API에 프롬프트를 보내고, 응답으로 포스트 내용을 생성합니다.  
  - 프롬프트는 `ai_service/prompt.txt`에 정의되어 있습니다.

- **자동 포스팅**  
  - `ai_post` 앱의 `auto_generate_post` 함수가 `/ai_post/post/` 경로로 요청을 받아, 내부적으로 `/ai_service/generate_post/` API를 호출하여 AI가 생성한 내용을 자동으로 게시합니다.  
  - 30분마다 `ai_post/scheduler.py`에 정의된 스케줄러가 실행되어 자동 포스팅 작업을 수행합니다.

- **블로그 CRUD 기능**  
  - 블로그 게시글의 생성, 조회, 수정, 삭제 기능은 `board` 앱에서 구현되어 있습니다.  
  - 주요 URL 경로:  
    ```
    rewrite_process/
    rewrite/
    delete/
    view/
    write_process/
    write/
    ```
  - 기본 블로그 메인 페이지는 `/` 경로에서 확인할 수 있습니다.

---

## 디렉토리 구조 (주요 파일)

ai_service/
 ├─ views.py           # OpenAI API 호출 및 포스트 생성 로직
 ├─ prompt.txt         # AI 프롬프트 템플릿

ai_post/
 ├─ views.py           # 자동 포스트 트리거 함수 (auto_generate_post)
 ├─ scheduler.py       # 30분마다 실행되는 스케줄러

board/
 ├─ views.py           # 블로그 CRUD 기능
 ├─ urls.py            # CRUD 관련 URL 패턴 정의

---


## 설치 및 실행

1. **환경설정**  
   - Python 3.x, Django 최신 버전 권장  
   - OpenAI API 키 환경변수 설정 필요 (`OPENAI_API_KEY`)

2. **의존성 설치**  
   ```bash
   pip install Django
   pip install requests
   pip install openai
   pip install apscheduler
