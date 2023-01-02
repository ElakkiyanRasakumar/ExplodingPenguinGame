import pygame
from math import *
from sys import exit


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load(
            "Assets/Graphics/Player/Basic Sprite.PNG").convert_alpha(), 0, 0.75)
        self.rect = self.image.get_rect(center=(200, 200))
        global playerXpos
        global playerYpos

    def player_movement(self):
        dy = 5
        dx = 5
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.y -= dy
        if keys[pygame.K_s]:
            self.rect.y += dy
        if keys[pygame.K_a]:
            self.rect.x -= dx
        if keys[pygame.K_d]:
            self.rect.x += dx

    def boundaries(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= 1000:
            self.rect.right = 1000
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= 800:
            self.rect.bottom = 800

    def update_global_player_pos(self):
        global playerXpos
        global playerYpos
        playerXpos = self.rect.centerx
        playerYpos = self.rect.centery

    def update(self):
        self.player_movement()
        self.boundaries()
        self.update_global_player_pos()


class Eyes(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Assets/Graphics/Player/Eyes.PNG").convert_alpha()
        self.rect = self.image.get_rect(center=(playerXpos + 2, playerYpos + 50))

    def eye_movement(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        distanceX = mouseX - self.rect.x
        distanceY = mouseY - self.rect.y
        if distanceX <= -80:
            distanceX = -80
        if distanceX >= 50:
            distanceX = 50
        if distanceY <= -80:
            distanceY = -80
        if distanceY >= 15:
            distanceY = 15
        # if distanceY
        self.rect.x -= distanceX / -12
        self.rect.y -= distanceY / -12
        pass

    def update(self):
        self.rect.center = (playerXpos + 2, playerYpos - 50)
        self.eye_movement()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load("Assets/Graphics/Penguin/Penguin Front 2.PNG").convert_alpha(), 0, 4)
        self.rect = self.image.get_rect(center=(600, 600))

    def ai(self):
        distanceX = playerXpos - self.rect.centerx
        distanceY = playerYpos - self.rect.centery
        speed = 5
        angle = atan2(distanceY, distanceX)
        enemyXdir = cos(angle)
        enemyYdir = sin(angle)
        print(enemyXdir, enemyYdir)
        self.rect.centerx += enemyXdir * speed
        self.rect.centery += enemyYdir * speed

    def boundaries(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= 1000:
            self.rect.right = 1000
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= 800:
            self.rect.bottom = 800

    def update(self):
        self.ai()
        self.boundaries()

pygame.init()
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Penguin Apocalypse")
clock = pygame.time.Clock()
screen.fill("#f0f49c")
playerXpos = 0
playerYpos = 0

# Class Group
player = pygame.sprite.GroupSingle()
player.add(Player())
eyes = pygame.sprite.GroupSingle()
eyes.add(Eyes())
enemy = pygame.sprite.GroupSingle()
enemy.add(Enemy())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill("#f8f4ec")

    player.update()
    player.draw(screen)

    eyes.update()
    eyes.draw(screen)

    enemy.update()
    enemy.draw(screen)

    pygame.display.update()
    clock.tick(60)

if __name__ == '__main__':
    print('PyCharm')
