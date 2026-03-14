# **고양이 키우고 싶은 심심한 사람...**

### **1. Docker Compose 실행**

프로젝트 루트에서 실행

```
docker compose up
```

### **2. 브라우저 접속**

```
http://localhost:8000
```

### **특징**

- 고양이 이미지 클릭 → 반응
- Snack 버튼 → 간식 먹기
- 상태 변화
    - pet_ear : 쓰다듬기
    - pet_snack : 간식
    - pet_sleep : 60초 방치

행동 시스템
쓰다듬기 → 호감도 +2
대화 → 호감도 +1
간식 → 호감도 +3 (10개 이상 패널티)
방치 → 호감도 -1

AI 행동
성격 랜덤 생성
최근 대화 3~4개 기억
호감도 기반 말투 변화

UI
하트 게이지
레벨 표시
성격 표시
말풍선 대화

---

### **개발 모드 (Hot Reload)**

현재 docker-compose.yml은 프로젝트 폴더를 컨테이너에 볼륨 마운트한다.

따라서 다음 파일을 수정하면 **컨테이너 재빌드 없이 바로 반영된다.**

- main.py
- static/index.html
- static/game.js
- static/assets/*

---
