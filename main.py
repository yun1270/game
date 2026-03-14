from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os, requests, time, random

app = FastAPI()

OLLAMA_URL=os.getenv("OLLAMA_URL","http://ollama:11434")
session=requests.Session()

state="idle"
snacks=0
affection=50
level=1

last_action=time.time()
last_chat=0
state_start=time.time()

personality=random.choice(["tsundere","lazy","friendly"])

messages=[
{
"role":"system",
"content":"너는 귀여운 집고양이다. 항상 15자 이내로 말한다."
}
]

app.mount("/static",StaticFiles(directory="static"),name="static")


@app.on_event("startup")
def warmup():
    try:
        session.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model":"llama3",
                "messages":[{"role":"user","content":"hi"}],
                "keep_alive":"1h",
                "options":{"num_predict":5}
            },
            timeout=10
        )
    except:
        pass


@app.get("/")
def root():
    return FileResponse("static/index.html")


def mood():
    if affection<30: return "경계"
    if affection<70: return "보통"
    return "애교"


@app.get("/cat")
def cat(q:str=""):

    global affection,last_chat,last_action,messages

    last_chat=time.time()
    last_action=time.time()

    if q:
        affection=min(100,affection+1)

        messages.append({
            "role":"user",
            "content":q
        })

    res=session.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model":"llama3",
            "messages":messages[-6:],
            "stream":False,
            "keep_alive":"1h",
            "options":{
                "num_predict":15,
                "temperature":0.8
            }
        }
    )

    data=res.json()

    if "message" not in data:
        return {"error":data}

    msg=data["message"]["content"].strip()

    messages.append({
        "role":"assistant",
        "content":msg
    })

    return {
        "message":msg,
        "affection":affection
    }


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
