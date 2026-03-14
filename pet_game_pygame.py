import pygame
import sys
import os
import time

pygame.init()

WIDTH = 300
HEIGHT = 300

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dot Cat")

clock = pygame.time.Clock()

ASSET_PATH = "assets"

def load_image(name, scale=0.1):
    path = os.path.join(ASSET_PATH, name)
    img = pygame.image.load(path).convert_alpha()

    w = int(img.get_width() * scale)
    h = int(img.get_height() * scale)

    return pygame.transform.scale(img, (w, h))


pet_idle = load_image("pet.PNG")
pet_ear = load_image("pet_ear.PNG")
pet_sleep = load_image("pet_sleep.PNG")
pet_snack = load_image("pet_snack.PNG")

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


# 하트를 직접 그리는 함수
def draw_heart(surface, x, y):
    color = (255,100,120)

    pygame.draw.circle(surface, color, (x, y), 4)
    pygame.draw.circle(surface, color, (x+6, y), 4)

    pygame.draw.polygon(surface, color, [
        (x-2, y+2),
        (x+8, y+2),
        (x+3, y+10)
    ])


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

    if state == "ear" and now - state_start_time > 1:
        current_image = pet_idle
        state = "idle"

    if state == "snack" and now - state_start_time > 1:
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
        draw_heart(screen, x + pet_size//2 - 3, y - 8)

    # sleep 상태 Z 애니메이션
    if state == "sleep":
        z_text = z_font.render("Z",True,(120,120,120))
        screen.blit(z_text,(x + pet_size//2,y - 15 - z_offset))
        z_offset = (z_offset + 0.3) % 10

    # 간식 버튼
    pygame.draw.rect(screen,(200,200,200),button_rect)
    text = font.render("Snack",True,(0,0,0))
    screen.blit(text,(button_rect.x+15,button_rect.y+7))

    # 간식 횟수 표시 (원하면 활성화)
    # counter = font.render(f"Snacks: {snack_count}",True,(0,0,0))
    # screen.blit(counter,(10,10))

    pygame.display.flip()

    clock.tick(60)
