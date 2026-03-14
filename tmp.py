from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import requests
import time

app = FastAPI()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
state = "idle"
snacks = 0
last_action = time.time()
state_start = time.time()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return FileResponse("static/index.html")

@app.get("/cat")
def cat_talk():

    prompt = """
너는 귀여운 집고양이다.
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
        return {
            "error": data
        }

    return {"message": data["response"]}

@app.get("/state")
def get_state():
    global state

    now = time.time()

    # ear / snack 상태는 1초 유지
    if state in ["ear", "snack"] and now - state_start > 1:
        state = "idle"

    # 60초 방치 → sleep
    if state == "idle" and now - last_action > 60:
        state = "sleep"

    return {"state": state, "snacks": snacks}


@app.post("/pet")
def pet():
    global state, last_action, state_start

    if state == "sleep":
        state = "idle"
    else:
        state = "ear"

    last_action = time.time()
    state_start = time.time()

    return {"ok": True}


@app.post("/snack")
def snack():
    global state, snacks, last_action, state_start

    snacks += 1
    state = "snack"
    last_action = time.time()
    state_start = time.time()

    return {"ok": True}
