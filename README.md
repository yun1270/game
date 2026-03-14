### Start

1. 위치:
    
    ```
    cd ~/Desktop/game
    ```
    
2. 프로젝트 폴더에서 가상환경 생성
    
    ```
    python3 -m venv venv
    ```
    
    그러면 현재 폴더에 venv 디렉터리가 생성된다.
    
3. 가상환경 활성화
    
    ```
    source venv/bin/activate
    ```
    
    프롬프트가 다음처럼 바뀐다.
    
    ```
    (venv) ➜ study
    ```
    
4. 이제 패키지 설치
    
    ```
    pip install -r requirements.txt
    ```
    
    이때 Pygame이 가상환경에 설치된다. 시스템 Python에는 영향을 주지 않는다.
    
5. 게임 실행
    
    ```
    python pet_game.py
    ```
    
    가상환경이 활성화된 상태에서 실행해야 한다.
    
6. 종료
    
    ```bash
    deactivate
    ```
---

1. 이미지 빌드
```bash
docker build -t dotcat-dev .
```

2. 컨테이너 실행
```bash
docker run \
-p 8000:8000 \
-v $(pwd):/app \
dotcat-dev
```
---

docker-compose.yml
```bash
docker compose up
```
---

http://localhost:8000
