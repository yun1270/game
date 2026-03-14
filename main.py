from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import time

app = FastAPI()

state = "idle"
snacks = 0
last_action = time.time()
state_start = time.time()

app.mount("/static", StaticFiles(directory="static"), name="static")


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
