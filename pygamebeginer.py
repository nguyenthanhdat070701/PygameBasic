from genericpath import isfile
from main import HEALTH_FONT, WHITE, WINNER_FONT
import pygame
import os

from pygame.constants import K_d, K_s, K_w

pygame.font.init()

FBS = 60
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("control player and basic star!!!")

TAN = (255, 204, 102)
BLACK = (20, 20, 20)
C_RED = (200, 20, 2)
C_YELLOW = (0, 200, 200)
WHITE = (0, 0, 0)
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

SHIP_WIDTH, SHIP_HEIGHT = 45, 50

YELLOW_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
RED_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
YELLOW = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT)), 90
)
RED = pygame.transform.rotate(
    pygame.transform.scale(RED_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT)), 90 + 180
)
VEL = 5
BUL_VEL = 7
MAX_BUL = 2

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)


def yellow_control(keys_pressed, yellow, yellow_bul):
    if keys_pressed[pygame.K_a] and yellow.x > 0:
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + yellow.width < BORDER.x:
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y > 0:
        yellow.y -= VEL
        for bullet in yellow_bul:
            bullet.y -= VEL + 1
    if keys_pressed[pygame.K_s] and yellow.y + yellow.height < HEIGHT:
        yellow.y += VEL
        for bullet in yellow_bul:
            bullet.y += VEL + 1


def red_control(keys_pressed, red, red_bul):
    if keys_pressed[pygame.K_LEFT] and red.x - 5 > BORDER.x:
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + red.width < WIDTH:
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y > 0:
        red.y -= VEL
        for bullet in red_bul:
            bullet.y -= VEL + 1
    if keys_pressed[pygame.K_DOWN] and red.y + red.height < HEIGHT:
        red.y += VEL
        for bullet in red_bul:
            bullet.y += VEL + 1


def daw_br(yellow, red, yellow_bul, red_bul, yellow_health, red_health):
    WIN.fill(TAN)
    pygame.draw.rect(WIN, BLACK, BORDER)
    text_yellow = HEALTH_FONT.render("YELLOW:" + str(yellow_health), 1, BLACK)
    WIN.blit(text_yellow, (10, 10))
    text_red = HEALTH_FONT.render("RED:" + str(red_health), 1, BLACK)
    WIN.blit(text_red, (WIDTH - text_red.get_width() - 10, 10))
    WIN.blit(YELLOW, (yellow.x, yellow.y))
    WIN.blit(RED, (red.x, red.y))

    for bullet in red_bul:
        pygame.draw.rect(WIN, C_RED, bullet)
    for bullet in yellow_bul:
        pygame.draw.rect(WIN, C_YELLOW, bullet)
    pygame.display.update()


def handle_bul(yellow_bul, red_bul, yellow, red):
    for bullet in yellow_bul:
        bullet.x += BUL_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bul.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bul.remove(bullet)

    for bullet in red_bul:
        bullet.x -= BUL_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bul.remove(bullet)
        elif bullet.x < 0:
            red_bul.remove(bullet)


def draw_winner(winner_text):
    draw_text = WINNER_FONT.render(winner_text, 1, WHITE)
    WIN.blit(
        draw_text,
        (
            WIDTH / 2 - draw_text.get_width() / 2,
            HEIGHT / 2 - draw_text.get_height() / 2,
        ),
    )
    pygame.display.update()
    pygame.time.delay(3200)


def main():
    yellow = pygame.Rect(200, 250, SHIP_WIDTH, SHIP_HEIGHT)
    red = pygame.Rect(650, 250, SHIP_WIDTH, SHIP_HEIGHT)

    yellow_bul = []
    red_bul = []
    yellow_health = 5
    red_health = 5

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FBS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bul) < MAX_BUL:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width,
                        yellow.y + yellow.height // 2 - 2,
                        10,
                        5,
                    )
                    yellow_bul.append(bullet)

                if event.key == pygame.K_RCTRL and len(red_bul) < MAX_BUL:
                    bullet = pygame.Rect(
                        red.x + red.width, red.y + red.height // 2 - 2, 10, 5
                    )
                    red_bul.append(bullet)
            if event.type == RED_HIT:
                red_health -= 1

            if event.type == YELLOW_HIT:
                yellow_health -= 1
            winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        key_pressed = pygame.key.get_pressed()
        yellow_control(key_pressed, yellow, yellow_bul)
        red_control(key_pressed, red, red_bul)

        handle_bul(yellow_bul, red_bul, yellow, red)
        daw_br(yellow, red, yellow_bul, red_bul, yellow_health, red_health)
    main()


if __name__ == "__main__":
    main()
