import pygame
from sys import exit
import math


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load("Assets/Graphics/Basic Sprite.PNG").convert_alpha(), 0, 0.75)
        self.rect = self.image.get_rect(center=(500, 400))
        global playerXpos
        global playerYpos

    def player_movement(self):
        dy = 10
        dx = 10
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


    def update(self):
        self.player_movement()
        self.boundaries()
        global playerXpos
        global playerYpos
        playerXpos = self.rect.centerx
        playerYpos = self.rect.centery
class Eyes(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Assets/Graphics/Eyes.PNG").convert_alpha()
        self.rect = self.image.get_rect(center = (playerXpos + 50, playerYpos + 50))

    def update(self):
        self.rect.center = (playerXpos + 5, playerYpos - 50)


pygame.init()
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Penguin Apocalypse")
clock = pygame.time.Clock()
screen.fill("#f0f49c")
playerXpos = 0
playerYpos = 0
# Player Class Group
player = pygame.sprite.GroupSingle()
player.add(Player())
eyes = pygame.sprite.GroupSingle()
eyes.add(Eyes())
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

    pygame.display.update()
    clock.tick(60)

if __name__ == '__main__':
    print('PyCharm')
