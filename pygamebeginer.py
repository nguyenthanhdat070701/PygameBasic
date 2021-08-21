from genericpath import isfile
import pygame
import os

from pygame.constants import K_d, K_s, K_w
FBS = 60
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("control player and basic star!!!")

TAN = (255, 204, 102)
BLACK = (0, 0, 0)

BORDER = pygame.Rect(WIDTH/2 - 5, 0, 10, HEIGHT)

SHIP_WIDTH, SHIP_HEIGHT = 55, 40

YELLOW_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
RED_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
YELLOW = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT)), 90)
RED = pygame.transform.rotate(
    pygame.transform.scale(RED_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT)), 90+180)
VEL = 5


def daw_br(yellow, red):
    pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.fill(TAN)
    WIN.blit(YELLOW, (yellow.x, yellow.y))
    WIN.blit(RED, (red.x, red.y))
    pygame.display.update()


def yellow_control(keys_pressed, yellow):
    if keys_pressed[pygame.K_a]:
        yellow.x -= VEL
    if keys_pressed[pygame.K_d]:
        yellow.x += VEL
    if keys_pressed[pygame.K_w]:
        yellow.y -= VEL
    if keys_pressed[pygame.K_s]:
        yellow.y += VEL


def red_control(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT]:
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT]:
        red.x += VEL
    if keys_pressed[pygame.K_UP]:
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN]:
        red.y += VEL


def main():
    yellow = pygame.Rect(250, 200, SHIP_WIDTH, SHIP_HEIGHT)
    red = pygame.Rect(750, 200, SHIP_WIDTH, SHIP_HEIGHT)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FBS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        daw_br(yellow, red)
        key_pressed = pygame.key.get_pressed()
        yellow_control(key_pressed, yellow)
        red_control(key_pressed, red)
    pygame.quit()


if __name__ == "__main__":
    main()
