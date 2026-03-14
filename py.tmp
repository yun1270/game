from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import requests
import time

app = FastAPI()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")

state = "idle"

snacks = 0
affection = 50
level = 1

last_action = time.time()
last_chat = 0
state_start = time.time()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return FileResponse("static/index.html")


def affection_level():
    if affection < 30:
        return "경계"
    if affection < 70:
        return "보통"
    return "애교"


@app.get("/cat")
def cat_talk(q: str = ""):
    global last_action, last_chat, affection

    last_action = time.time()
    last_chat = time.time()

    mood = affection_level()

    if q:
        affection = min(100, affection + 1)

        prompt = f"""
너는 귀여운 집고양이다.
현재 호감도는 {affection}/100 이다.
관계 상태는 {mood} 이다.

사람의 말에 짧게 대답한다.
대사는 최대 15자.

사람: {q}
고양이:
"""
    else:
        prompt = f"""
너는 귀여운 집고양이다.
현재 사람에 대한 호감도는 {affection}/100 이다.
관계 상태는 {mood} 이다.

플레이어에게 15자 이내로 한마디 한다.
"""

    res = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    data = res.json()

    if "response" not in data:
        return {"error": data}

    return {
        "message": data["response"].strip(),
        "affection": affection
    }


@app.get("/state")
def get_state():
    global state, affection, level

    now = time.time()

    if state in ["ear", "snack"] and now - state_start > 1:
        state = "idle"

    if now - last_chat < 15:
        if state == "sleep":
            state = "idle"

    if state == "idle" and now - last_action > 60:
        state = "sleep"
        affection = max(0, affection - 1)

    level = 1 + affection // 25

    return {
        "state": state,
        "snacks": snacks,
        "affection": affection,
        "level": level
    }


@app.post("/pet")
def pet():
    global state, last_action, state_start, affection

    if state == "sleep":
        state = "idle"
    else:
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
