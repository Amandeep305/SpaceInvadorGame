import pygame
import random
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((900, 600))

background = pygame.image.load("space.png")

pygame.display.set_caption("Space Invador")
icon = pygame.image.load("001-ufo-flying.png")
pygame.display.set_icon(icon)

playerIcon = pygame.image.load("space-invaders.png")
playerX = 450
playerY = 490
playerX_change = 0

enemyIcon = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemy = 6

for i in range(num_of_enemy):
    enemyIcon.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0, 836))
    enemyY.append(random.randint(50, 100))
    enemyX_change.append(2)
    enemyY_change.append(0)

bulletIcon = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 490
bulletX_change = 0
bulletY_change = 0
bullet_state = "ready"

score_value = 0
font = pygame.font.Font("freesansbold.ttf", 30)
textX = 10
textY = 10

mixer.music.load("background.wav")
mixer.music.play(-1)

over = pygame.font.Font("freesansbold.ttf", 64)

def score(x, y):
    score = font.render(f"Score: {score_value}", True, (255, 255, 255))
    screen.blit(score, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletIcon, (x+16 , y+10))

def player(x, y):
    screen.blit(playerIcon, (x, y))

def enemy(x, y, i):
    screen.blit(enemyIcon[i], (x, y))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    dist = ((enemyX-bulletX)**2 + (enemyY-bulletY)**2) ** 0.5
    if dist<=27:
        return True
    return False

def game_over():
    gover = over.render("GAME OVER", True, (255, 255, 255))
    screen.blit(gover, (250, 300))

running = True
while running:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change -= 2
            if event.key == pygame.K_RIGHT:
                playerX_change += 2
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet = mixer.Sound("laser.wav")
                    bullet.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 836:
        playerX = 836

    for i in range(num_of_enemy):
        if enemyY[i] > 450:
            for j in range(num_of_enemy):
                enemyY[j] = 2000
            game_over()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX[i] = 0
            enemyX_change[i] = 2
            enemyX[i] += enemyX_change[i]
            enemyY_change[i] = 40
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 836:
            enemyX[i] = 836
            enemyX_change[i] = -2
            enemyX[i] += enemyX_change[i]
            enemyY_change[i] = 40
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosive = mixer.Sound("explosion.wav")
            explosive.play()
            bulletY = 490
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 836)
            enemyY[i] = random.randint(50, 100)

        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = 490
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= 5

    score(textX, textY)
    player(playerX, playerY) 
    pygame.display.update()