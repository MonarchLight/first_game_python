import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
import random
import os

pygame.init()

HEIGHT = 600
WIDTH = 800

FONT = pygame.font.SysFont("Verdana", 20)
FPS = pygame.time.Clock()

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)

main_surface = pygame.display.set_mode((WIDTH, HEIGHT))

back_ground = pygame.transform.scale(
    pygame.image.load("background.png"),  (WIDTH, HEIGHT))
back_ground_x1 = 0
back_ground_x2 = back_ground.get_width()
back_ground_move = 1

IMAGE_PATH = "goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

player = pygame.image.load("player.png").convert_alpha()
player_size = (player.get_width(), player.get_height())
player_rect = player.get_rect(center=(player_size[0]-75, HEIGHT/2))
player_move_down = [0, 1]
player_move_up = [0, -1]
player_move_left = [-1, 0]
player_move_right = [1, 0]


def create_enemy():
    enemy = pygame.image.load("enemy.png").convert_alpha()
    enemy_size = (enemy.get_width(), enemy.get_height())
    enemy_rect = pygame.Rect(WIDTH, random.randint(
        enemy_size[1], HEIGHT-enemy_size[1]), *enemy_size)
    enemy_move = [random.randint(-6, -2), 0]
    return [enemy, enemy_rect, enemy_move]


def create_bonus():
    bonus = pygame.image.load("bonus.png").convert_alpha()
    bonus_size = (bonus.get_width(), bonus.get_height())
    bonus_rect = pygame.Rect(random.randint(
        bonus_size[0], WIDTH-bonus_size[0]),  -bonus_size[1], *bonus_size)
    bonus_move = [0, random.randint(1, 3)]
    return [bonus, bonus_rect, bonus_move]


CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 2000)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 5000)

SCOREBOARD = pygame.USEREVENT + 3
pygame.time.set_timer(SCOREBOARD, 1000)

CHANGE_IMAGE = pygame.USEREVENT + 4
pygame.time.set_timer(CHANGE_IMAGE, 150)

score = 0
image_index = 0

enemies = []
bonuses = []
playing = True
game_over = False

while playing:
    FPS.tick(120)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == SCOREBOARD:
            score += 1
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(
                IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0

        if event.type == pygame.KEYDOWN and game_over:
            enemies.clear()
            bonuses.clear()
            player_rect.center = (player_size[0]-75, HEIGHT/2)
            score = 0
            back_ground_move = 1
            player_move_down = [0, 1]
            player_move_up = [0, -1]
            player_move_left = [-1, 0]
            player_move_right = [1, 0]
            game_over = False

    if not game_over:
        back_ground_x1 -= back_ground_move
        back_ground_x2 -= back_ground_move

        main_surface.blit(back_ground, (back_ground_x1, 0))
        main_surface.blit(back_ground, (back_ground_x2, 0))

        if back_ground_x1 < -back_ground.get_width():
            back_ground_x1 = back_ground.get_width()

        if back_ground_x2 < -back_ground.get_width():
            back_ground_x2 = back_ground.get_width()

        keys = pygame.key.get_pressed()

        if keys[K_DOWN] and player_rect.bottom < HEIGHT:
            player_rect = player_rect.move(player_move_down)

        if keys[K_UP] and player_rect.top > 0:
            player_rect = player_rect.move(player_move_up)

        if keys[K_LEFT] and player_rect.left > 0:
            player_rect = player_rect.move(player_move_left)

        if keys[K_RIGHT] and player_rect.right < WIDTH:
            player_rect = player_rect.move(player_move_right)

        for enemy in enemies:
            enemy[1] = enemy[1].move(enemy[2])
            main_surface.blit(enemy[0], enemy[1])

            if enemy[1].right < 0:
                enemies.remove(enemy)

            if player_rect.colliderect(enemy[1]):
                game_over = True

        for bonus in bonuses:
            bonus[1] = bonus[1].move(bonus[2])
            main_surface.blit(bonus[0], bonus[1])

            if bonus[1].bottom > HEIGHT:
                bonuses.remove(bonus)

            if player_rect.colliderect(bonus[1]):
                if player_move_down[1] < 3:
                    back_ground_move += 1
                    player_move_down[1] += 1
                    player_move_up[1] -= 1
                    player_move_left[0] -= 1
                    player_move_right[0] += 1

                bonuses.remove(bonus)

        main_surface.blit(FONT.render(
            str(score), True, COLOR_BLACK), (WIDTH-50, 20))
        main_surface.blit(player, player_rect)

    else:
        main_surface.blit(back_ground, (0, 0))
        font = pygame.font.SysFont('Arial', 50)
        text = font.render('Game Over', True, COLOR_RED)
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        main_surface.blit(text, text_rect)

    pygame.display.flip()
