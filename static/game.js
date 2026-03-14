// static/game.js

const canvas = document.getElementById("game")
const ctx = canvas.getContext("2d")

const images = {
  idle: new Image(),
  ear: new Image(),
  sleep: new Image(),
  snack: new Image()
}

images.idle.src = "/static/assets/pet.PNG"
images.ear.src = "/static/assets/pet_ear.PNG"
images.sleep.src = "/static/assets/pet_sleep.PNG"
images.snack.src = "/static/assets/pet_snack.PNG"

let state = "idle"
let affection = 50
let level = 1
let personality = "friendly"
let mood = "보통"

const catX = 75
const catY = 50
const catW = 150
const catH = 150

function getCurrentImage() {
  return images[state] || images.idle
}

function draw() {
  ctx.clearRect(0, 0, 300, 300)

  const img = getCurrentImage()

  if (img.complete) {
    ctx.drawImage(img, catX, catY, catW, catH)
  }
}

function updateUI() {
  const heartsEl = document.getElementById("hearts")
  const levelEl = document.getElementById("level")
  const personalityEl = document.getElementById("personality")
  const moodEl = document.getElementById("mood")

  let heartCount = Math.floor(affection / 20)
  heartCount = Math.max(0, Math.min(5, heartCount))

  let hearts = ""
  for (let i = 0; i < 5; i++) {
    hearts += i < heartCount ? "❤" : "♡"
  }

  heartsEl.innerText = hearts
  levelEl.innerText = "Lv." + level
  personalityEl.innerText = personality
  moodEl.innerText = mood
}

async function update() {
  try {
    const res = await fetch("/state")
    const data = await res.json()

    state = data.state || "idle"
    affection = data.affection ?? 50
    level = data.level ?? 1
    personality = data.personality || "friendly"
    mood = data.mood || "보통"

    draw()
    updateUI()
  } catch (e) {
    console.error("state update failed", e)
  }
}

canvas.addEventListener("click", async (e) => {
  const rect = canvas.getBoundingClientRect()

  const x = e.clientX - rect.left
  const y = e.clientY - rect.top

  if (
    x > catX &&
    x < catX + catW &&
    y > catY &&
    y < catY + catH
  ) {
    try {
      await fetch("/pet", { method: "POST" })
      await update()
    } catch (e) {
      console.error("pet failed", e)
    }
  }
})

async function snack() {
  try {
    await fetch("/snack", { method: "POST" })
    await update()
  } catch (e) {
    console.error("snack failed", e)
  }
}

Object.values(images).forEach((img) => {
  img.onload = () => draw()
})

update()
setInterval(update, 500)
