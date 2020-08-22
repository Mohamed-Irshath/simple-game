import random as rand
import math

import pygame as pg
from pygame import mixer


# Initializing
pg.init()
pg.font.init()

# Gaming window
screen = pg.display.set_mode((800, 600))


# background music
pg.mixer.music.load('background.wav')
pg.mixer.music.play(-1)

# Caption and Icon
pg.display.set_caption('COVID-19')
# icon = pg.image.load('virus.ico')
# pg.display.set_icon(icon)
background_img = pg.image.load('backgroundimg.png')

# Player
player_img = pg.image.load('hand-sanitizer.png')
playerX = 364
playerY = 480
playerX_change = 0

# Enemy
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_img.append(pg.image.load('coronavirus.png'))
    enemyX.append(rand.randint(0, 736))
    enemyY.append(rand.randint(0, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)

# Bullet
bullet_img = pg.image.load('drop1.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 9
bullet_state = "ready"

over_font = pg.font.SysFont('arial', 64)
over_font2 = pg.font.SysFont('arial', 32)
over_font3 = pg.font.SysFont('arial', 16)
# over_font = pg.font.Font('freesansbold.ttf', 64)
# over_font2 = pg.font.Font('freesansbold.ttf', 32)
# over_font3 = pg.font.Font('freesansbold.ttf', 16)

score_value = 0
font = pg.font.SysFont('arial', 32)


# functions
def game_over_text():
    game_over = over_font.render("GAME OVER", True, (255, 255, 255))
    game_over2 = over_font2.render("INFECTED!! QUARANTINE YOURSELF", True, (255, 0, 0))
    game_over3 = over_font3.render("CREATED BY IRSHATH WITH HELP OF SOME TUTORIALS", True, (0, 255, 0))
    screen.blit(game_over, (200, 250))
    screen.blit(game_over2, (100, 310))
    screen.blit(game_over3, (150, 350))


def show_score():
    score = font.render("score:" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (10, 10))


def player():
    screen.blit(player_img, (playerX, playerY))


def enemy(x, y):
    screen.blit((enemy_img[i]), (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))


def iscollision(x, y, w, z):
    distance_formula = math.sqrt((math.pow(x - w, 2)) + (math.pow(y - z, 2)))
    if distance_formula <= 27:
        return True
    else:
        return False


# Game loop
running = True
while running:
    screen.blit(background_img, (0, 0))
    screen.fill((0, 0, 0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                playerX_change -= 5
            if event.key == pg.K_RIGHT:
                playerX_change += 5
            if event.key == pg.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                playerX_change = 0
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 734:
        playerX = 734

    for i in range(num_of_enemies):
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            bullet_state = "ready"
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 734:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            score_value += 1
            bulletY = 480
            bullet_state = "ready"

            enemyX[i] = rand.randint(0, 736)
            enemyY[i] = rand.randint(0, 150)
        enemy(enemyX[i], enemyY[i])
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player()
    show_score()
    pg.display.update()
