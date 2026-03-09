import pygame
import sys
import os
import time

pygame.init()

WIDTH = 360
HEIGHT = 360

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dot Cat")

clock = pygame.time.Clock()

ASSET_PATH = "assets"

def load_image(name, scale=0.25):
    path = os.path.join(ASSET_PATH, name)
    img = pygame.image.load(path).convert_alpha()

    w = int(img.get_width() * scale)
    h = int(img.get_height() * scale)

    return pygame.transform.scale(img, (w, h))

pet_idle = load_image("pet.png")
pet_ear = load_image("pet_ear.png")
pet_sleep = load_image("pet_sleep.png")
pet_snack = load_image("pet_snack.png")

pet_size = pet_idle.get_width()

x = WIDTH // 2 - pet_size // 2
y = HEIGHT // 2 - pet_size // 2

current_image = pet_idle
state = "idle"

last_click_time = time.time()
state_start_time = time.time()

snack_count = 0

button_rect = pygame.Rect(WIDTH//2 - 40, HEIGHT - 50, 80, 30)

font = pygame.font.SysFont(None,20)
z_font = pygame.font.SysFont(None,24)

z_offset = 0

while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_pos = pygame.mouse.get_pos()

            if button_rect.collidepoint(mouse_pos):

                current_image = pet_snack
                state = "snack"
                state_start_time = time.time()
                last_click_time = time.time()
                snack_count += 1

            else:

                pet_rect = pygame.Rect(x,y,pet_size,pet_size)

                if pet_rect.collidepoint(mouse_pos):

                    if state == "sleep":
                        current_image = pet_idle
                        state = "idle"

                    else:
                        current_image = pet_ear
                        state = "ear"
                        state_start_time = time.time()

                    last_click_time = time.time()

    now = time.time()

    if state == "ear" and now - state_start_time > 3:
        current_image = pet_idle
        state = "idle"

    if state == "snack" and now - state_start_time > 2:
        current_image = pet_idle
        state = "idle"

    if state == "idle" and now - last_click_time > 60:
        current_image = pet_sleep
        state = "sleep"

    screen.fill((255,255,255))

    screen.blit(current_image,(x,y))

    mouse_pos = pygame.mouse.get_pos()
    pet_rect = pygame.Rect(x,y,pet_size,pet_size)

    # 마우스 올리면 하트 표시
    if pet_rect.collidepoint(mouse_pos):
        heart = font.render("♥",True,(255,100,120))
        screen.blit(heart,(x + pet_size//2 - 5,y - 10))

    # sleep 상태 Z 애니메이션
    if state == "sleep":
        z_text = z_font.render("Z",True,(120,120,120))
        screen.blit(z_text,(x + pet_size//2,y - 15 - z_offset))
        z_offset = (z_offset + 0.3) % 10

    # 간식 버튼
    pygame.draw.rect(screen,(200,200,200),button_rect)
    text = font.render("Snack",True,(0,0,0))
    screen.blit(text,(button_rect.x+15,button_rect.y+7))

    # 간식 횟수 표시
    counter = font.render(f"Snacks: {snack_count}",True,(0,0,0))
    screen.blit(counter,(10,10))

    pygame.display.flip()

    clock.tick(60)
