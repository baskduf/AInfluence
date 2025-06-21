# myapp/scheduler.py

import atexit
import requests
from apscheduler.schedulers.background import BackgroundScheduler

def call_auto_generate_post():
    url = "http://localhost:8000/ai_post/post/"
    # try:
    #     response = requests.post(url, timeout=500)
    #     print(f"[스케줄러] auto_generate_post 호출 성공, 상태 코드: {response.status_code}")
    # except Exception as e:
    #     print(f"[스케줄러] auto_generate_post 호출 실패: {e}")
    # print("test")

def start():
    scheduler = BackgroundScheduler()

    from datetime import datetime

    # scheduler.add_job(call_auto_generate_post, 'interval', minutes=30, next_run_time=datetime.now())
    scheduler.add_job(call_auto_generate_post, 'interval', minutes=800)
    scheduler.start()

    jobs = scheduler.get_jobs()
    print(f"[스케줄러] 등록된 잡: {jobs}")

    atexit.register(lambda: scheduler.shutdown())
