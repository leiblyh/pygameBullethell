import os
from re import T
import time
from typing_extensions import Self
import pygame
import random

#Initializing pygame, game loop.
pygame.init()
running = True
framerate = 60
clock = pygame.time.Clock()
path = os.getcwd()

#Settings variables
drawHitboxes = True
playMusic = True

#Setting game window
gameWindow = pygame.display.set_mode((800, 1200))
pygame.display.set_caption('Bullethell Test Game')

#Additional global variables
spriteSize = (90, 135)
lockout = 0
projTimer = 0
projSpeed = 8
projRadius = 20
enemySpeed = 5
canFire = True
enemyHP = 200
damage = enemyHP / 25

#Module classes.
class Player (pygame.sprite.Sprite):
    def __init__(self, startpos, velocity):
        super().__init__()
        self.pos = pygame.math.Vector2(startpos)
        self.lockout = 0
        self.xSpeed = self.ySpeed = 0
        self.velocity = velocity
        self.images = [pygame.image.load(path + "\\resources\\player\\player_back.png"), pygame.image.load(path + "\\resources\\player\\player_forward.png"),
        pygame.image.load(path + "\\resources\\player\\player_left.png"), pygame.image.load(path + "\\resources\\player\\player_right.png")]
        for img in self.images:
            img.set_colorkey((255,255,255))
            img.convert_alpha()
        self.image = pygame.transform.scale(self.images[0], spriteSize)
        self.rect = self.image.get_rect(center = (round(self.pos.x), round(self.pos.y)))

    def update(self):
        keys = pygame.key.get_pressed()
        self.lockout += 1
        if keys[ord('w')]:
            self.ySpeed -= self.velocity
            self.image = pygame.transform.scale(self.images[0], spriteSize)
        if keys[ord('s')]:
            self.ySpeed += self.velocity
            self.image = pygame.transform.scale(self.images[1], spriteSize)
        if keys[ord('a')]:
            self.xSpeed -= self.velocity
            self.image = pygame.transform.scale(self.images[2], spriteSize)
        if keys[ord('d')]:
            self.xSpeed += self.velocity
            self.image = pygame.transform.scale(self.images[3], spriteSize)
        if keys[ord(' ')]:
            if self.lockout >= 30:
                self.shoot()
                self.lockout = 0


        self.rect.x += self.xSpeed
        self.rect.y += self.ySpeed
        self.xSpeed = self.ySpeed = 0

        self.pos = pygame.math.Vector2(self.rect.x, self.rect.y)

        if drawHitboxes == True:
            pygame.draw.rect(gameWindow, (255, 0, 0), pygame.Rect(self.rect.left, self.rect.top, self.rect.width, self.rect.height), 1)

    def restrict(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= gameWindow.get_width():
            self.rect.right = gameWindow.get_width()
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= gameWindow.get_height():
            self.rect.bottom = gameWindow.get_height()
    
    def shoot(self):
        projectile = Projectile(pygame.math.Vector2(player.pos), projSpeed, projRadius, (random.randint(-5, 5), -45), 1)
        projectiles.add(projectile)

class Enemy (pygame.sprite.Sprite):
    def __init__(self, startpos, starthp):
        super().__init__()
        self.pos = pygame.math.Vector2(startpos)
        self.hp = starthp
        self.image = pygame.image.load(path + "\\resources\\enemy.png")
        self.image = pygame.transform.scale(self.image, (spriteSize[0]*3, spriteSize[1]*2))
        self.image.set_colorkey((255,255,255))
        self.image.convert_alpha()
        self.rect = self.image.get_rect(center = (round(self.pos.x), round(self.pos.y)))

    def update(self):
        if drawHitboxes:
            pygame.draw.rect(gameWindow, (255, 0, 0), pygame.Rect(self.rect.left, self.rect.top, self.rect.width, self.rect.height), 1)

class HealthBar (pygame.sprite.Sprite):
    def __init__(self, x, y, inithealth):
        super().__init__()
        self.pos = (x,y)
        self.health = inithealth
        self.rect = pygame.rect.Rect(x, y, 25, 200)
        self.image = pygame.image.load(path + "\\resources\\evil-among-us.png")

    def update(self, change):
        self.health = self.health - change
    


class Projectile (pygame.sprite.Sprite):
    def __init__(self, startpos, velocity, radius, startdir, type):
        super().__init__()
        self.pos = pygame.math.Vector2(startpos)
        self.velocity = velocity
        self.dir = pygame.math.Vector2(startdir).normalize()
        self.type = type
        if self.type == 0:
            self.image = pygame.image.load(path + "\\resources\\bad_bullet.png")
        else:
            self.image = pygame.image.load(path + "\\resources\\good_bullet.png").convert()
        self.image.set_colorkey((255,255,255))
        self.image.convert_alpha()
        self.image = pygame.transform.scale(self.image, (radius * 2, radius * 2))
        self.rect = self.image.get_rect(center = (self.pos.x, self.pos.y))

    def update(self):
        self.pos += self.dir * self.velocity
        self.rect.center = round(self.pos.x), round(self.pos.y)

        if self.rect.right < 0 or self.rect.left > gameWindow.get_width() or self.rect.bottom < 0 or self.rect.top > gameWindow.get_height():
            projectiles.remove(self)

        if drawHitboxes == True:
            pygame.draw.rect(gameWindow, (255, 0, 0), pygame.Rect(self.rect.left, self.rect.top, self.rect.width, self.rect.height), 1)



#Main methods.
def gameOver():
        pygame.mixer.music.pause()
        font = pygame.font.Font(path + "\\resources\\COMIC.TTF", 40)
        texts = font.render("Game Over!", True, (0,0,0)), font.render("Remaining Boss HP: " + str((enemy.hp/200)*100) + " %", True, (0,0,0))
        textX = gameWindow.get_width() / 2
        textY = gameWindow.get_height() / 2
        gameWindow.blit(texts[0], [textX - (texts[0].get_rect().width/2), textY])
        gameWindow.blit(texts[1], [textX - (texts[1].get_rect().width/2), textY + 50])
        pause = True
        pygame.display.update()

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

def victory():
    pygame.mixer.music.pause()
    pygame.draw.rect(gameWindow, (0,0,0), pygame.Rect(enemy.rect.left-20, enemy.rect.top - 60, enemyHP, 50), 0) 
    font = pygame.font.Font(path + "\\resources\\COMIC.TTF", 40)
    text = font.render("You won!", True, (0,0,0))
    textX = gameWindow.get_width() / 2
    textY = gameWindow.get_height() / 2
    gameWindow.blit(text, [textX - (text.get_rect().width/2), textY])
    pause = True
    pygame.display.update()
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    

if playMusic:
    pygame.mixer.music.load(path + "\\resources\\bgmusic.mp3")
    pygame.mixer.music.set_volume(0.02)
    pygame.mixer.music.play()


entities = pygame.sprite.Group()
projectiles = pygame.sprite.Group()

start = (gameWindow.get_width()/2, 200)
enemy = Enemy(start, enemyHP)
entities.add(enemy)

start, velocity = (350, 800), 10
player = Player(start, velocity)
entities.add(player)

#Game loop
while running:
    clock.tick(framerate)
    projTimer += framerate
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.restrict()

    if projTimer == (framerate) * 10:
        projectile = Projectile(pygame.math.Vector2(enemy.pos), projSpeed, projRadius, (random.randint(-45,45), 45), 0)
        projectiles.add(projectile)
        projTimer = 0

    gameWindow.fill("#751100")
    entities.draw(gameWindow)
    projectiles.draw(gameWindow)
    entities.update()
    projectiles.update()
    pygame.draw.rect(gameWindow, (0,0,0), pygame.Rect(gameWindow.get_width()/2 - (enemyHP/2), enemy.rect.top - 60, enemyHP, 50), 0) 
    pygame.draw.rect(gameWindow, (255,0,0), pygame.Rect(gameWindow.get_width()/2 - (enemyHP/2), enemy.rect.top - 60, enemy.hp, 50), 0) 
    pygame.display.update()

    for projectile in projectiles:
        if projectile.rect.colliderect(player.rect) and projectile.type == 0:
            gameOver()
        if projectile.rect.colliderect(enemy.rect) and projectile.type == 1:
            enemy.hp -= damage
            projectiles.remove(projectile)
            print(enemy.hp)
        if enemy.hp <= 0:
            victory()
