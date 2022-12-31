import pygame
from sys import exit


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load("Hero_Still.png").convert_alpha(), 0, 0.75)
        self.rect = self.image.get_rect(center=(500, 400))

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


pygame.init()
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Penguin Apocalypse")
clock = pygame.time.Clock()
screen.fill("#58c4d4")

# Player Class Group
player = pygame.sprite.GroupSingle()
player.add(Player())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill("#58c4d4")
    player.update()
    player.draw(screen)

    pygame.display.update()
    clock.tick(60)

if __name__ == '__main__':
    print('PyCharm')
