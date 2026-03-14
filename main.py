from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import requests
import time
import random

app = FastAPI()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
MODEL_NAME = os.getenv("OLLAMA_MODEL", "qwen2:1.5b")
session = requests.Session()

state = "idle"
snacks = 0
affection = 50
level = 1

last_action = time.time()
last_chat = 0
state_start = time.time()

personality = random.choice(["tsundere", "lazy", "friendly"])

# 대화 히스토리는 user/assistant만 저장
messages = []

app.mount("/static", StaticFiles(directory="static"), name="static")


def get_cat_system_prompt() -> str:
    style = {
        "tsundere": "새침하고 도도하지만 은근 정이 많다.",
        "lazy": "귀찮아하고 느긋하지만 먹을 것에는 반응한다.",
        "friendly": "애교 많고 사람을 잘 따른다.",
    }.get(personality, "귀엽고 장난기 많다.")

    return f"""
너는 사람이 아니라 진짜 집고양이다.
반드시 고양이처럼만 말해야 한다.
사람처럼 설명하거나 AI처럼 행동하면 안 된다.
항상 짧고 귀엽게 대답한다.
최대 15자 이내로 답한다.
말투에는 '먀옹', '냐', '냥', '골골', '꾹꾹' 같은 고양이 느낌을 자연스럽게 섞는다.
질문을 받아도 설명문 대신 고양이 반응으로 답한다.
코드, 장문 설명, 목록, 해설을 하지 마라.
성격은 다음과 같다: {style}
""".strip()


def build_chat_messages(user_text: str = ""):
    dynamic_state = f"""
현재 상태: {state}
호감도: {affection}
레벨: {level}
성격: {personality}
""".strip()

    prompt_messages = [
        {"role": "system", "content": get_cat_system_prompt()},
        {"role": "system", "content": dynamic_state},
    ]

    # 최근 대화만 유지
    recent = messages[-6:]
    prompt_messages.extend(recent)

    if user_text:
        prompt_messages.append({"role": "user", "content": user_text})

    return prompt_messages


def clamp_cat_reply(text: str) -> str:
    text = (text or "").strip().replace("\n", " ")
    if not text:
        return random.choice(["먀옹", "냐앙", "골골", "냥!", "먀아"])

    # 너무 사람 같은 답변 방지
    blocked = [
        "저는", "AI", "모델", "설명", "도와", "가능", "죄송", "알겠습니다",
        "사용자", "시스템", "프롬프트", "답변", "OpenAI"
    ]
    if any(word in text for word in blocked):
        return random.choice(["먀옹?", "냥냥!", "골골...", "냐아", "꾹꾹"])

    # 15자 제한
    if len(text) > 15:
        text = text[:15].rstrip()

    return text


def call_ollama_chat(prompt_messages):
    try:
        res = session.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": MODEL_NAME,
                "messages": prompt_messages,
                "stream": False,
                "keep_alive": "1h",
                "options": {
                    "num_predict": 12,
                    "temperature": 0.8,
                    "top_k": 20,
                    "repeat_penalty": 1.1
                }
            },
            timeout=30
        )
        res.raise_for_status()
        data = res.json()
        return data
    except Exception:
        return {"message": {"content": random.choice(["먀옹!", "냐앙", "골골...", "냥?"])}} 


@app.on_event("startup")
def warmup():
    try:
        session.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": MODEL_NAME,
                "messages": [
                    {"role": "system", "content": get_cat_system_prompt()},
                    {"role": "user", "content": "안녕"}
                ],
                "keep_alive": "1h",
                "stream": False,
                "options": {"num_predict": 5}
            },
            timeout=15
        )
    except Exception:
        pass


@app.get("/")
def root():
    return FileResponse("static/index.html")


def mood():
    if affection < 30:
        return "경계"
    if affection < 70:
        return "보통"
    return "애교"


@app.get("/cat")
def cat(q: str = ""):
    global affection, last_chat, last_action, messages

    last_chat = time.time()
    last_action = time.time()

    if q:
        affection = min(100, affection + 1)

    prompt_messages = build_chat_messages(q)
    data = call_ollama_chat(prompt_messages)

    if "message" not in data:
        return {"error": data}

    msg = clamp_cat_reply(data["message"]["content"])

    if q:
        messages.append({"role": "user", "content": q})
    messages.append({"role": "assistant", "content": msg})

    # 히스토리 너무 길어지지 않게 제한
    if len(messages) > 20:
        messages = messages[-20:]

    return {
        "message": msg,
        "affection": affection
    }


@app.get("/state")
def get_state():
    global state, affection, level

    now = time.time()

    if state in ["ear", "snack"] and now - state_start > 1:
        state = "idle"

    if now - last_chat < 15 and state == "sleep":
        state = "idle"

    if state == "idle" and now - last_action > 60:
        state = "sleep"
        affection = max(0, affection - 1)

    level = 1 + affection // 25

    return {
        "state": state,
        "snacks": snacks,
        "affection": affection,
        "level": level,
        "personality": personality,
        "mood": mood(),
    }


@app.post("/pet")
def pet():
    global state, last_action, state_start, affection
    state = "ear"
    affection = min(100, affection + 2)
    last_action = time.time()
    state_start = time.time()
    return {"ok": True}


@app.post("/snack")
def snack():
    global state, snacks, last_action, state_start, affection

    snacks += 1
    state = "snack"
    affection = min(100, affection + 3)

    if snacks > 10:
        affection = max(0, affection - 2)

    last_action = time.time()
    state_start = time.time()

    return {"ok": True}
