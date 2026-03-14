# **Dot Cat**

간단한 고양이 펫 게임, 두 가지 방식으로 실행할 수 있다.

1. **Pygame 데스크톱 버전**
2. **Docker + FastAPI 웹 버전**

---

## **1. Pygame 로컬 실행**

Python 가상환경에서 Pygame을 사용해 게임을 실행하는 방식이다.

### **1. 프로젝트 폴더 이동**

```
cd ~/Desktop/game
```

### **2. 가상환경 생성**

```
python3 -m venv venv
```

### **3. 가상환경 활성화**

```
source venv/bin/activate
```

프롬프트 예시

```
(venv) ➜ game
```

### **4. 패키지 설치**

```
pip install -r requirements.txt
```

### **5. 게임 실행**

```
python pygame.py
```

### **6. 가상환경 종료**

```
deactivate
```

---

## **2. Docker 웹 버전 실행**

이 버전은 FastAPI 서버와 브라우저 렌더링을 사용하며

컨테이너는 Docker로 실행한다.

### **1. Docker Compose 실행**

프로젝트 루트에서 실행

```
docker compose up
```

처음 실행 시 이미지 빌드가 자동으로 진행된다.

### **2. 브라우저 접속**

```
http://localhost:8000/static/index.html
```

### **특징**

- 고양이 이미지 클릭 → 반응
- Snack 버튼 → 간식 먹기
- 상태 변화
    - pet_ear : 쓰다듬기
    - pet_snack : 간식
    - pet_sleep : 60초 방치

---

### **개발 모드 (Hot Reload)**

현재 docker-compose.yml은 프로젝트 폴더를 컨테이너에 볼륨 마운트한다.

따라서 다음 파일을 수정하면 **컨테이너 재빌드 없이 바로 반영된다.**

- main.py
- static/index.html
- static/game.js
- static/assets/*

---

### **프로젝트 구조**

```
.
├── main.py
├── pygame.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── static
│   ├── index.html
│   ├── game.js
│   └── assets
│       ├── pet.PNG
│       ├── pet_ear.PNG
│       ├── pet_sleep.PNG
│       └── pet_snack.PNG
```

---
