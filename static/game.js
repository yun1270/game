// static/game.js

const canvas=document.getElementById("game")
const ctx=canvas.getContext("2d")

const images={
idle:new Image(),
ear:new Image(),
sleep:new Image(),
snack:new Image()
}

images.idle.src="/static/assets/pet.PNG"
images.ear.src="/static/assets/pet_ear.PNG"
images.sleep.src="/static/assets/pet_sleep.PNG"
images.snack.src="/static/assets/pet_snack.PNG"

let state="idle"
let affection=50
let level=1

const catX=75
const catY=50
const catW=150
const catH=150

function draw(){
ctx.clearRect(0,0,300,300)
ctx.drawImage(images[state],catX,catY,catW,catH)
}

function updateUI(){

const hearts=document.getElementById("hearts")
const levelText=document.getElementById("level")
const personality=document.getElementById("personality")

let heartCount=Math.floor(affection/20)
let h=""

for(let i=0;i<5;i++){
h+=i<heartCount?"❤":"♡"
}

hearts.innerText=h
levelText.innerText="Lv."+level

}

async function update(){

const res=await fetch("/state")
const data=await res.json()

state=data.state
affection=data.affection
level=data.level

document.getElementById("personality").innerText="성격: "+data.personality

draw()
updateUI()

}

canvas.addEventListener("click",async e=>{

const rect=canvas.getBoundingClientRect()

const x=e.clientX-rect.left
const y=e.clientY-rect.top

if(
x>catX &&
x<catX+catW &&
y>catY &&
y<catY+catH
){
await fetch("/pet",{method:"POST"})
}

})

async function snack(){
await fetch("/snack",{method:"POST"})
}

setInterval(update,200)
