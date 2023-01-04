import pygame
from math import *
from sys import exit
from random import randint


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_list = ["Assets/Graphics/Player/Basic Sprite.PNG",
                            "Assets/Graphics/Player/Basic Sprite 2.PNG",
                            "Assets/Graphics/Player/Basic Sprite 3.PNG",
                            "Assets/Graphics/Player/Basic Sprite 4.PNG"]
        self.player_list_index = 0

        self.image = pygame.transform.rotozoom(
            pygame.image.load(self.player_list[self.player_list_index]).convert_alpha(), 0, 0.75)
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
        self.animation()

    def animation(self):
        if self.player_list_index <= 3:
            self.player_list_index += .05
        else:
            self.player_list_index = 0
        self.image = pygame.transform.rotozoom(
            pygame.image.load(self.player_list[int(self.player_list_index)]).convert_alpha(), 0, 0.75)


class Eyes(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Assets/Graphics/Player/Eyes.PNG").convert_alpha()
        self.rect = self.image.get_rect(center=(0, 0))

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
        self.rect.x -= distanceX / -12
        self.rect.y -= distanceY / -12

    def update(self):
        self.target()
        self.eye_movement()
        # self.target() sets the position, and then self.eye_movement() moves it within the boundaries

    def target(self):
        if game_active:
            self.rect.center = (playerXpos + 2, playerYpos - 50)

        if not game_active:
            self.rect.center = (start_menu_player_rect.centerx + 2, start_menu_player_rect.centery - 75)
            pass


class Enemy(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, velocity):
        super().__init__()
        self.image = pygame.transform.rotozoom(
            pygame.image.load("Assets/Graphics/Penguin/Penguin Front 2.PNG").convert_alpha(), 0, 4)
        self.rect = self.image.get_rect(center=(xpos, ypos))
        self.velocity = velocity

    def pathing(self):
        distanceX = playerXpos - self.rect.centerx
        distanceY = playerYpos - self.rect.centery
        angle = atan2(distanceY, distanceX)
        enemyXdir = cos(angle)
        enemyYdir = sin(angle)
        self.rect.centerx += enemyXdir * self.velocity
        self.rect.centery += enemyYdir * self.velocity

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
        self.pathing()
        self.boundaries()


class Gun(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Assets/Graphics/Player/Gun Left.PNG").convert_alpha()
        self.rect = self.image.get_rect(center=(playerXpos + 20, playerYpos))

    def update_pos(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        distanceX = self.rect.centerx - mouseX
        distanceY = self.rect.centery - mouseY
        angle = degrees(atan2(distanceY, distanceX))
        if mouseX > playerXpos:
            self.image = pygame.transform.rotate(
                pygame.image.load("Assets/Graphics/Player/Gun Right.PNG").convert_alpha(), angle)
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(center=(playerXpos + 30, playerYpos))

        else:
            self.image = pygame.transform.rotate(
                pygame.image.load("Assets/Graphics/Player/Gun Right.PNG").convert_alpha(), -angle)
            self.rect = self.image.get_rect(center=(playerXpos - 20, playerYpos))

    def update(self):
        self.update_pos()


def sprite_collision():
    global enemies
    if pygame.sprite.spritecollide(player.sprite, enemy, True):
        enemies -= 1
    pass


# Init and Setup
pygame.init()
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Penguin Apocalypse")
clock = pygame.time.Clock()
screen.fill("#f0f49c")
go_up = False
go_down = True
max_enemies = 4
enemies = 0

# Global Variables
playerXpos = 0
playerYpos = 0
game_active = False
font = pygame.font.Font("Assets/Font/Preahvihear-Regular.ttf", 75)
font_smaller = pygame.font.Font("Assets/Font/Preahvihear-Regular.ttf", 50)

# Game Screen Init
start_menu_font = font.render("Penguin Apocalypse", True, "Black")
start_menu_font_rect = start_menu_font.get_rect(center=(500, 200))
start_menu_font_space = font_smaller.render("Press Space To Play", True, "Black")
start_menu_font_space_rect = start_menu_font_space.get_rect(center=(500, 600))

start_menu_player_list = ["Assets/Graphics/Player/Basic Sprite.PNG", "Assets/Graphics/Player/Basic Sprite 2.PNG",
                          "Assets/Graphics/Player/Basic Sprite 3.PNG", "Assets/Graphics/Player/Basic Sprite 4.PNG"]
start_menu_player_list_index = 0
start_menu_player = pygame.image.load(start_menu_player_list[start_menu_player_list_index])
start_menu_player_rect = start_menu_player.get_rect(center=(500, 410))

# Class Group
player = pygame.sprite.GroupSingle()
player.add(Player())
eyes = pygame.sprite.GroupSingle()
eyes.add(Eyes())
enemy = pygame.sprite.Group()
gun = pygame.sprite.GroupSingle()
gun.add(Gun())

animation_timer = pygame.USEREVENT + 1
pygame.time.set_timer(animation_timer, 1000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
        if not game_active:
            if event.type == animation_timer:
                if start_menu_player_list_index <= 2:
                    start_menu_player_list_index += 1
                else:
                    start_menu_player_list_index = 0
                start_menu_player = pygame.image.load(start_menu_player_list[start_menu_player_list_index])
                screen.blit(start_menu_player, start_menu_player_rect)

    if game_active:
        screen.fill("#f8f4ec")
        player.update()
        player.draw(screen)

        eyes.update()
        eyes.draw(screen)

        gun.update()
        gun.draw(screen)

        enemy.update()
        enemy.draw(screen)

        sprite_collision()

        if enemies <= max_enemies:
            enemy.add(Enemy(randint(0, 1000), randint(0, 800), randint(2, 5)))
            enemies += 1

    else:
        screen.fill("#f8f4ec")
        screen.blit(start_menu_font, start_menu_font_rect)
        screen.blit(start_menu_font_space, start_menu_font_space_rect)
        screen.blit(start_menu_player, start_menu_player_rect)
        eyes.update()
        eyes.draw(screen)
        if go_down:
            start_menu_font_rect.centery += 1
        if start_menu_font_rect.centery == 220:
            go_down = False
            go_up = True
        if go_up:
            start_menu_font_rect.centery -= 1
        if start_menu_font_rect.centery == 200:
            go_down = True
            go_up = False

    pygame.display.update()
    if not game_active:
        clock.tick(25)
    else:
        clock.tick(60)

if __name__ == '__main__':
    print('PyCharm')
