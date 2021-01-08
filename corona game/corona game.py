import math
import random

import pygame
from pygame import mixer
mixer.get_init()
pygame.init()
# screen decorating....
screen = pygame.display.set_mode((800, 500))
background = pygame.image.load("background.png")
pygame.display.set_caption("COVID-19-Corona 2.0")
icon = pygame.image.load("title.png")
pygame.display.set_icon(icon)

# players and enemies initials
playerimg = pygame.image.load("player.png")
enemy1img = []
enemy1X = []
enemy1Y = []
enemy1X_change = []
enemy1Y_change = []
num_enemy_1 = 3
num_enemy_2 = 3
enemy_speed = 5
for i in range(num_enemy_1):
    enemy1img.append(pygame.image.load("enemy.png"))
    enemy1X.append(random.randint(15, 770))
    enemy1Y.append(random.randint(50, 150))
    enemy1X_change.append(enemy_speed)
    enemy1Y_change.append(0)
enemy2img = []
enemy2X = []
enemy2Y = []
enemy2X_change = []
for i in range(num_enemy_2):
    enemy2img.append(pygame.image.load("enemy.png"))
    enemy2X.append(random.randint(15, 770))
    enemy2Y.append(random.randint(50, 150))
    enemy2X_change.append(enemy_speed)
playerX = 385
playerY = 435
playerX_change = 0
playerY_change = 0

# bullet issentials
bulletimg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = playerY
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"


# enemy clash game over
def crash():
    crash_distance1 = math.sqrt(math.pow(enemy2Y[i] - playerY, 2) + math.pow(enemy2X[i] - playerX, 2))
    crash_distance2 = math.sqrt(math.pow(enemy1Y[i] - playerY, 2) + math.pow(enemy1X[i] - playerX, 2))
    if crash_distance1 <= 30 or crash_distance2 <= 30:
        return True


def player(x, y):
    screen.blit(playerimg, (round(x), round(y)))


def enemy1(x, y):
    screen.blit(enemy1img[i], (round(x), round(y)))


def enemy2(x, y):
    screen.blit(enemy2img[i], (round(x), round(y)))


def bullet_fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (round(x), round(y)))


def is_collision():
    distance = math.sqrt(math.pow(enemy1X[i] - bulletX, 2) + (math.pow(enemy1Y[i] - bulletY, 2)))
    if distance <= 25:
        return True


def is_collision2():
    distance2 = math.sqrt(math.pow(enemy2X[i] - bulletX, 2) + (math.pow(enemy2Y[i] - bulletY, 2)))
    if distance2 <= 25:
        return True


# game ending function
alignX = 345
alignY = 250
font = pygame.font.Font('freesansbold.ttf', 72)


def msg():
    msg_given = font.render("GAME OVER!!!", True, (255, 0, 0))
    score_result = font.render("Total Score=" + str(score_value), True, (255, 10, 100))
    screen.blit(msg_given, (100, 210))
    screen.blit(score_result, (120, 280))


score_value = 0
pygame.font.init()
font1 = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10


def is_score(x, y):
    score = font1.render("Points :" + str(score_value), True, (255, 0, 0))
    screen.blit(score, (x, y))


mixer.music.load('background.wav')
mixer.music.play(-1)
running = True
player_speed = 7
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -(player_speed + score_value * 0.05)
            if event.key == pygame.K_RIGHT:
                playerX_change = (player_speed + score_value * 0.05)
            if event.key == pygame.K_UP:
                playerY_change = -(player_speed + score_value * 0.05)
            if event.key == pygame.K_DOWN:
                playerY_change = +(player_speed + score_value * 0.05)
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet = mixer.Sound('bullet.wav')
                    bullet.play()
                    bulletX = playerX
                    bulletY = playerY
                    bullet_fire(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.type == pygame.K_RIGHT or pygame.K_LEFT:
                playerX_change = 0.001
            if event.type == pygame.K_RIGHT or pygame.K_LEFT:
                playerY_change = 0.001
    playerX += playerX_change
    playerY += playerY_change
    if playerY <= 258:
        playerY = 258
    elif playerY >= 600:
        playerY = 600
    if playerX <= 0:
        playerX = 0
    elif playerX >= 738:
        playerX = 738
    for i in range(num_enemy_1):
        if enemy1Y[i] >= 450 or enemy2Y[i] >= 450 or crash():
            for j in range(num_enemy_1):
                enemy1Y[j] += 2000
                enemy2Y[j] += 2000
                msg()
                mixer.music.stop()
            break
        enemy1X[i] += enemy1X_change[i]
        if enemy1X[i] <= 0:
            enemy1X_change[i] = enemy_speed + score_value * 0.1
            enemy1Y[i] += 20
        elif enemy1X[i] >= 764:
            enemy1X_change[i] = -(enemy_speed + score_value * 0.1)
            enemy1Y[i] += 20
        collision = is_collision()
        if collision:
            explosion = mixer.Sound('collision.wav')
            explosion.play()
            enemy1X[i] = random.randint(15, 765)
            enemy1Y[i] = random.randint(25, 150)
            score_value += 1
        enemy2X[i] += enemy2X_change[i]
        if enemy2X[i] <= 0:
            enemy2X_change[i] = enemy_speed + score_value * 0.1
            enemy2Y[i] += 20
        elif enemy2X[i] >= 764:
            enemy2X_change[i] = -(enemy_speed + score_value * 0.1)
            enemy2Y[i] += 20
        collision2 = is_collision2()
        if collision2:
            explosion = mixer.Sound('collision.wav')
            explosion.play()
            enemy2X[i] = random.randint(15, 765)
            enemy2Y[i] = random.randint(25, 150)
            score_value += 1
        player(playerX, playerY)
        enemy1(enemy1X[i], enemy1Y[i])
        enemy2(enemy2X[i], enemy2Y[i])
    if bullet_state == "fire":
        bullet_fire(bulletX, bulletY)
        bulletY -= 30
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = playerY

    is_score(textX, textY)

    pygame.display.update()
