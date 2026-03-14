# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os, requests, time, random

app = FastAPI()

OLLAMA_URL = os.getenv("OLLAMA_URL","http://ollama:11434")

state="idle"
snacks=0
affection=50
level=1

last_action=time.time()
last_chat=0
state_start=time.time()

personality=random.choice(["tsundere","lazy","friendly"])
memory=[]

app.mount("/static",StaticFiles(directory="static"),name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")

def affection_level():
    if affection<30: return "경계"
    if affection<70: return "보통"
    return "애교"

def personality_text():
    if personality=="tsundere":
        return "겉으로는 퉁명하지만 사실은 관심이 많다."
    if personality=="lazy":
        return "게으르고 귀찮아하지만 은근히 애교 있다."
    return "사람을 좋아하고 장난기 많다."

def random_behavior():
    global state,state_start
    r=random.random()
    if r<0.03:
        state="ear"
        state_start=time.time()
    elif r<0.06:
        state="snack"
        state_start=time.time()

@app.get("/cat")
def cat_talk(q:str=""):
    global last_action,last_chat,affection,memory

    last_action=time.time()
    last_chat=time.time()

    mood=affection_level()

    history=""
    for h in memory[-4:]:
        history+=f"사람:{h[0]}\n고양이:{h[1]}\n"

    if q:
        affection=min(100,affection+1)

        prompt=f"""
너는 귀여운 집고양이다.
성격: {personality_text()}
호감도: {affection}/100 ({mood})

대사는 15자 이내.

이전 대화:
{history}

사람:{q}
고양이:
"""
    else:
        prompt=f"""
너는 귀여운 집고양이다.
성격: {personality_text()}
호감도: {affection}/100 ({mood})

플레이어에게 짧게 한마디 한다.
"""

    res=requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model":"llama3",
            "prompt":prompt,
            "stream":False
        }
    )

    data=res.json()

    if "response" not in data:
        return {"error":data}

    msg=data["response"].strip()

    if q:
        memory.append((q,msg))
        memory=memory[-6:]

    return {"message":msg,"affection":affection}

@app.get("/state")
def get_state():
    global state,affection,level

    now=time.time()

    if state in ["ear","snack"] and now-state_start>1:
        state="idle"

    if now-last_chat<15 and state=="sleep":
        state="idle"

    if state=="idle" and now-last_action>60:
        state="sleep"
        affection=max(0,affection-1)

#    random_behavior()

    level=1+affection//25

    return {
        "state":state,
        "snacks":snacks,
        "affection":affection,
        "level":level,
        "personality":personality
    }

@app.post("/pet")
def pet():
    global state,last_action,state_start,affection
    state="ear"
    affection=min(100,affection+2)
    last_action=time.time()
    state_start=time.time()
    return {"ok":True}

@app.post("/snack")
def snack():
    global state,snacks,last_action,state_start,affection

    snacks+=1
    state="snack"

    affection=min(100,affection+3)

    if snacks>10:
        affection=max(0,affection-2)

    last_action=time.time()
    state_start=time.time()

    return {"ok":True}
