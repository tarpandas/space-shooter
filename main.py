import pygame
import random
import math
from pygame import mixer

# initialize pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800,600))

# title and icon
pygame.display.set_caption("Space invader")
icon = pygame.image.load('./image_assets/icon.png')
pygame.display.set_icon(icon)

# adding background
backgroundImg = pygame.image.load('./image_assets/background.jpg')

# adding background music
mixer.music.load('./audio_assets/kubbi_digestive_biscuit.mp3')
mixer.music.play(-1) # -1 to play in loop

# score
score = 0
font = pygame.font.Font('./font_assets/retro_gaming.ttf',24)

textX = 10
textY = 10
    
def show_score(x,y):
    score_value = font.render("Score: " + str(score), True, (255,255,255))
    screen.blit(score_value, (x,y))
    
    # show instructions
    instr_to_move = font.render("<- and -> to move", True, (150,150,255))
    instr_to_shoot = font.render("'spacebar' to shoot", True, (150,150,255))
    screen.blit(instr_to_move, (10,550))
    screen.blit(instr_to_shoot, (500,550))
# game over
go_font = pygame.font.Font('./font_assets/retro_gaming.ttf',64)

def game_over_text():
    game_over = go_font.render("Game Over", True, (255, 0, 0))
    screen.blit(game_over, (200,250))
    
    game_over = font.render("Developed by Tarpan Das", True, (255, 255, 0))
    screen.blit(game_over, (420,10))

# player
playerImg = pygame.image.load('./image_assets/player.png')
playerX = 370
playerY = 450
player_mov_var = 1.5
playerX_change = 0

def player(x,y):
    screen.blit(playerImg,(x, y)) # blit() means draw

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
number_of_enemies = 6
enemyX_change_speed = []

for i in range(number_of_enemies):
    enemyImg.append(pygame.image.load('./image_assets/enemy.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.5)
    enemyX_change_speed.append(0.5)
    enemyY_change.append(30)

def enemy(x, y, i):
    screen.blit(enemyImg[i],(x, y))
    
# bullet
bulletImg = pygame.image.load('./image_assets/bullet.png')
bulletX = 0
bulletY = 450 # top of player
bulletY_change = 2 
# ready state - the bullet is not moving
# fire state - the bullet is currently moving
bullet_state = "ready"

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))
    
# collision detection
"""
Distance formula:
d^2 = (x2 - x1)^2 + (y2 - y1)^2
where d is the distance between two points (x1, y1) and (x2, y2) in a 2D space
"""
def isCollision(enemyX, enemyY, bulletX, bulletY):
    x2 = math.pow((enemyX - bulletX),2)
    y2 = math.pow((enemyY - bulletY),2)
    distance = math.sqrt(x2 + y2)
    if(distance < 27):
        return True
        
    return False

# game logic
running = True
while running:

    # filling in our background in rgb format
    screen.fill((10,0,10))
    
    # backgound image
    screen.blit(backgroundImg, (0,0))
    
    # creating an event to close the game window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -player_mov_var
            if event.key == pygame.K_RIGHT:
                playerX_change = player_mov_var
            # bullet fire
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX # helps keep the bullet at launch position
                    fire_bullet(playerX, bulletY)
                    # bullet fire sound
                    bullet_sound = mixer.Sound('./audio_assets/laser.mp3')
                    bullet_sound.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    
    # player movement restriction
    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736
    
    # enemy movement restrictions
    for i in range(number_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = enemyX_change_speed[i] 
            enemyY[i]+= enemyY_change[i]
        if enemyX[i] >= 736:
            enemyX_change[i] = -enemyX_change_speed[i] 
            enemyY[i] += enemyY_change[i]
            
        # collision
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            bulletY = 450
            bullet_state = "ready"
            score += 1
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)
            
            # explosion sound
            explosion_sound = mixer.Sound('./audio_assets/boom.mp3')
            explosion_sound.play()
                
        # game over
        if enemyY[i] >= 400: # 450
            for j in range(number_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        # enemy draw
        enemy(enemyX[i], enemyY[i], i)
    
    # player draw
    player(playerX, playerY)
    
    # bullet movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    
    # bullet destroy
    if bulletY <= 0:
        bulletY = playerY + 10
        bullet_state = "ready"
    
    # show score
    show_score(textX, textY)
    
    # updating display with each loop
    pygame.display.update()