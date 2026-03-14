const canvas = document.getElementById("game")
const ctx = canvas.getContext("2d")

const images = {
 idle: new Image(),
 ear: new Image(),
 sleep: new Image(),
 snack: new Image()
}

images.idle.src="/static/assets/pet.PNG"
images.ear.src="/static/assets/pet_ear.PNG"
images.sleep.src="/static/assets/pet_sleep.PNG"
images.snack.src="/static/assets/pet_snack.PNG"

let state="idle"

const catX=75
const catY=50
const catW=150
const catH=150

function draw(){

 ctx.clearRect(0,0,300,300)

 const img=images[state]
 ctx.drawImage(img,catX,catY,catW,catH)
}

async function update(){

 const res=await fetch("/state")
 const data=await res.json()

 state=data.state
 draw()
}

canvas.addEventListener("click",async (e)=>{

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
