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
messages = []

app.mount("/static", StaticFiles(directory="static"), name="static")


def get_cat_system_prompt() -> str:
    style = {
        "tsundere": "새침하고 도도하지만 은근 정이 많다.",
        "lazy": "귀찮아하고 느긋하지만 먹을 것에는 반응한다.",
        "friendly": "애교 많고 사람을 잘 따른다.",
    }.get(personality, "귀엽고 장난기 많다.")

    return f"""
너는 진짜 집고양이다.
항상 고양이처럼 짧게 말한다.
최대 10자 이내로 답한다.
사람처럼 설명하지 마라.
'먀옹', '냥', '냐', '골골' 같은 말투를 쓴다.
성격: {style}
""".strip()


def build_chat_messages(user_text: str = ""):
    dynamic_state = f"현재 상태:{state}, 호감도:{affection}, 레벨:{level}, 성격:{personality}"

    prompt_messages = [
        {"role": "system", "content": get_cat_system_prompt()},
        {"role": "system", "content": dynamic_state},
    ]

    # 최근 히스토리 최소화: 속도에 가장 중요
    prompt_messages.extend(messages[-4:])

    if user_text:
        prompt_messages.append({"role": "user", "content": user_text})

    return prompt_messages


def clamp_cat_reply(text: str) -> str:
    text = (text or "").strip().replace("\n", " ")
    if not text:
        return random.choice(["먀옹", "냥!", "골골", "냐앙"])

    if len(text) > 10:
        text = text[:10].rstrip()

    banned = ["저는", "AI", "설명", "도와", "죄송", "사용자", "시스템"]
    if any(x in text for x in banned):
        return random.choice(["먀옹?", "냥냥!", "골골...", "냐아"])

    return text


def call_ollama_chat(prompt_messages):
    try:
        res = session.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": MODEL_NAME,
                "messages": prompt_messages,
                "stream": False,
                "keep_alive": "4h",
                "options": {
                    "num_predict": 8,
                    "num_ctx": 512,
                    "temperature": 0.7,
                    "top_k": 10,
                    "repeat_penalty": 1.05
                }
            },
            timeout=15
        )
        res.raise_for_status()
        return res.json()
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
                "stream": False,
                "keep_alive": "4h",
                "options": {
                    "num_predict": 4,
                    "num_ctx": 512
                }
            },
            timeout=10
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

    msg = clamp_cat_reply(data.get("message", {}).get("content", ""))

    if q:
        messages.append({"role": "user", "content": q})
    messages.append({"role": "assistant", "content": msg})

    if len(messages) > 12:
        messages = messages[-12:]

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
