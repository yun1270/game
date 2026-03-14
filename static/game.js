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

const catX = 75
const catY = 50
const catW = 150
const catH = 150

window.catBusy = false

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

  let heartCount = Math.floor(affection / 20)
  heartCount = Math.max(0, Math.min(5, heartCount))

  let hearts = ""
  for (let i = 0; i < 5; i++) {
    hearts += i < heartCount ? "❤" : "♡"
  }

  heartsEl.innerText = hearts
  levelEl.innerText = "Lv." + level
  personalityEl.innerText = personality
}

async function update() {
  try {
    const res = await fetch("/state")
    const data = await res.json()

    state = data.state || "idle"
    affection = data.affection ?? 50
    level = data.level ?? 1
    personality = data.personality || "friendly"

    draw()
    updateUI()
  } catch (e) {
    console.error("state update failed", e)
  }
}

canvas.addEventListener("click", async (e) => {
  if (window.catBusy) return

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
      window.catBusy = true
      document.getElementById("chatInput").disabled = true
      document.getElementById("sendButton").disabled = true
      document.getElementById("snackButton").disabled = true
      document.getElementById("busyText").innerText = "고양이를 쓰다듬는 중..."

      await fetch("/pet", { method: "POST" })
      await update()
    } catch (e) {
      console.error("pet failed", e)
    } finally {
      window.catBusy = false
      document.getElementById("chatInput").disabled = false
      document.getElementById("sendButton").disabled = false
      document.getElementById("snackButton").disabled = false
      document.getElementById("busyText").innerText = ""
      document.getElementById("chatInput").focus()
    }
  }
})

async function snack() {
  if (window.catBusy) return

  try {
    window.catBusy = true
    document.getElementById("chatInput").disabled = true
    document.getElementById("sendButton").disabled = true
    document.getElementById("snackButton").disabled = true
    document.getElementById("busyText").innerText = "고양이가 간식 먹는 중..."

    await fetch("/snack", { method: "POST" })
    await update()
  } catch (e) {
    console.error("snack failed", e)
  } finally {
    window.catBusy = false
    document.getElementById("chatInput").disabled = false
    document.getElementById("sendButton").disabled = false
    document.getElementById("snackButton").disabled = false
    document.getElementById("busyText").innerText = ""
    document.getElementById("chatInput").focus()
  }
}

Object.values(images).forEach((img) => {
  img.onload = () => draw()
})

update()
setInterval(() => {
  if (!window.catBusy) {
    update()
  }
}, 500)
