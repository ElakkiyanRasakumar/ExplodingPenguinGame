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
        self.image = pygame.image.load("Assets/Graphics/Penguin/Front 1.PNG").convert_alpha()
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
        global angle
        mouseX, mouseY = pygame.mouse.get_pos()
        distanceX = self.rect.centerx - mouseX
        distanceY = self.rect.centery - mouseY
        angle = degrees(atan2(distanceY, distanceX))
        if mouseX > playerXpos:
            if 180 > angle > 90:
                self.image = pygame.transform.rotate(
                    pygame.image.load("Assets/Graphics/Player/Gun Right.PNG").convert_alpha(), angle)
                self.image = pygame.transform.flip(self.image, False, True)
                self.rect = self.image.get_rect(bottomleft=(playerXpos, playerYpos + 13))
            else:
                self.image = pygame.transform.rotate(
                    pygame.image.load("Assets/Graphics/Player/Gun Right.PNG").convert_alpha(), angle)
                self.image = pygame.transform.flip(self.image, False, True)
                self.rect = self.image.get_rect(topleft=(playerXpos, playerYpos - 20))

        else:
            if 90 > angle > 0:
                self.image = pygame.transform.rotate(
                    pygame.image.load("Assets/Graphics/Player/Gun Right.PNG").convert_alpha(), -angle)
                self.rect = self.image.get_rect(bottomright=(playerXpos, playerYpos + 15))
            else:
                self.image = pygame.transform.rotate(
                    pygame.image.load("Assets/Graphics/Player/Gun Right.PNG").convert_alpha(), -angle)
                self.rect = self.image.get_rect(topright=(playerXpos, playerYpos - 20))

    def update_global_gun_pos(self):
        global gunXposLeft
        global gunYposLeft
        global gunXposBLeft
        global gunYposBLeft
        #
        global gunXposRight
        global gunYposRight
        global gunXposBRight
        global gunYposBRight

        xLeft, yLeft = self.rect.topleft
        xBLeft, yBLeft = self.rect.bottomleft
        xRight, yRight = self.rect.topright
        xBRight, yBRight = self.rect.bottomright

        gunXposLeft = xLeft
        gunYposLeft = yLeft
        gunXposBLeft = xBLeft
        gunYposBLeft = yBLeft

        gunXposRight = xRight
        gunYposRight = yRight
        gunXposBRight = xBRight
        gunYposBRight = yBRight

    def update(self):
        self.update_pos()
        self.update_global_gun_pos()


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        mouseX, mouseY = pygame.mouse.get_pos()
        self.image = pygame.transform.rotate(pygame.image.load("Assets/Graphics/Player/Bulllet.PNG").convert_alpha(),
                                             -angle + 180)
        if mouseX < playerXpos:
            if angle < 0:
                self.rect = self.image.get_rect(bottomleft=(gunXposBLeft, gunYposBLeft - 5))
            else:
                self.rect = self.image.get_rect(topleft=(gunXposLeft, gunYposLeft + 5))
        else:
            if angle < -90:
                self.rect = self.image.get_rect(bottomright=(gunXposBRight, gunYposBRight - 5))
            else:
                self.rect = self.image.get_rect(topright=(gunXposRight, gunYposRight + 5))

        self.x, self.y = self.rect.topleft
        distanceX = mouseX - self.rect.centerx
        distanceY = mouseY - self.rect.centery
        self.angle2 = atan2(distanceY, distanceX)
        self.dx = cos(self.angle2) * 10
        self.dy = sin(self.angle2) * 10

    def update_pos(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.topleft = (self.x, self.y)

    def boundaries(self):
        if self.rect.right > 1000:
            self.kill()
        if self.rect.right < 0:
            self.kill()
        if self.rect.bottom > 800:
            self.kill()
        if self.rect.top < 0:
            self.kill()

    def update(self):
        self.update_pos()
        self.boundaries()


class SpawningBullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load("Assets/Graphics/Collectable Bullet.PNG")
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        pass


class Hearts(pygame.sprite.Sprite):
    def __init__(self):
        super.__init__()
        pass

    def update(self):
        pass


def sprite_collision():
    global enemies
    global bullets
    global penguins_killed
    global game_active
    global heart_list_index
    global heart_list_index1
    global heart_list_index2
    global heart_list_index3
    global heart1
    global heart2
    global heart3
    if pygame.sprite.spritecollide(player.sprite, enemy, True):
        if heart_list_index3 > 0:
            game_active = False
        elif heart_list_index2 > 0:
            heart_list_index3 +=1
            heart3 = pygame.image.load(heart_list3[heart_list_index3])
        elif heart_list_index1 > 0:
            heart_list_index2 += 1
            heart2 = pygame.image.load(heart_list2[heart_list_index2])
        elif heart_list_index1 == 0:
            heart_list_index1 += 1
            heart1 = pygame.image.load(heart_list1[heart_list_index1])

    if pygame.sprite.groupcollide(bullet, enemy, True, True):
        enemies -= 1
        penguins_killed += 1
    if pygame.sprite.spritecollide(player.sprite, spawningBullets, True):
        bullets += 1


def penguin_shot():
    x = randint(0, 1000)
    y = randint(0, 800)
    if playerXpos - 200 < x < playerXpos + 200:
        x = randint(0, 1000)
    if playerYpos - 250 < y < playerYpos + 250:
        y = randint(0, 800)
    if len(enemy) < max_enemies:
        enemy.add(Enemy(x, y, randint(2, 4)))


# Init and Setup
pygame.init()
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Penguin Apocalypse")
pygame.display.set_icon(pygame.image.load("Assets/Graphics/Icon/Icon.jpg"))
clock = pygame.time.Clock()
screen.fill("#f0f49c")
go_up = False
go_down = True
max_enemies = 4
enemies = 0
bullets = 6
bullet_active = False
angle = 0
penguins_killed = 0
# Global Variables
playerXpos = 0
playerYpos = 0
gunXposLeft = 0
gunYposLeft = 0
gunXposBLeft = 0
gunYposBLeft = 0

gunXposRight = 0
gunYposRight = 0
gunXposBRight = 0
gunYposBRight = 0

game_active = False
font = pygame.font.Font("Assets/Font/Preahvihear-Regular.ttf", 75)
font_smaller = pygame.font.Font("Assets/Font/Preahvihear-Regular.ttf", 50)
counter_font = pygame.font.Font("Assets/Font/Preahvihear-Regular.ttf", 40)

# Game Screen Init
start_menu_font = font.render("Penguin Apocalypse", True, "Black")
start_menu_font_rect = start_menu_font.get_rect(center=(500, 200))
start_menu_font_space = font_smaller.render("Press Space To Play", True, "Black")
start_menu_font_space_rect = start_menu_font_space.get_rect(center=(500, 600))

# Bullet Couter
bullet_counter_font = counter_font.render(f"Bullets: {bullets}", True, "Black")
bullet_counter_font_rect = bullet_counter_font.get_rect(bottomright=(975, 800))

start_menu_player_list = ["Assets/Graphics/Player/Basic Sprite.PNG", "Assets/Graphics/Player/Basic Sprite 2.PNG",
                          "Assets/Graphics/Player/Basic Sprite 3.PNG", "Assets/Graphics/Player/Basic Sprite 4.PNG"]
start_menu_player_list_index = 0
start_menu_player = pygame.image.load(start_menu_player_list[start_menu_player_list_index])
start_menu_player_rect = start_menu_player.get_rect(center=(500, 410))

# Hearts
heart_list1 = ["Assets/Graphics/Heart/Life.PNG", "Assets/Graphics/Heart/No Life.PNG"]
heart_list_index1 = 0
heart1 = pygame.image.load(heart_list1[heart_list_index1])
heart1_rect = heart1.get_rect(topright=(975, 25))

heart_list2 = ["Assets/Graphics/Heart/Life.PNG", "Assets/Graphics/Heart/No Life.PNG"]
heart_list_index2 = 0
heart2 = pygame.image.load(heart_list2[heart_list_index2])
heart2_rect = heart2.get_rect(topright=(900, 25))

heart_list3 = ["Assets/Graphics/Heart/Life.PNG", "Assets/Graphics/Heart/No Life.PNG"]
heart_list_index3 = 0
heart3 = pygame.image.load(heart_list3[heart_list_index3])
heart3_rect = heart3.get_rect(topright=(825, 25))

heart_list_index = [heart_list_index1, heart_list_index2, heart_list_index3]

# Class Group
player = pygame.sprite.GroupSingle()
player.add(Player())
eyes = pygame.sprite.GroupSingle()
eyes.add(Eyes())
enemy = pygame.sprite.Group()
gun = pygame.sprite.GroupSingle()
gun.add(Gun())
bullet = pygame.sprite.Group()
spawningBullets = pygame.sprite.Group()

animation_timer = pygame.USEREVENT + 1
pygame.time.set_timer(animation_timer, 1000)

bullet_spawn_timer = pygame.USEREVENT + 1
pygame.time.set_timer(bullet_spawn_timer, 500)

while True:
    if game_active:
        screen.fill("#f8f4ec")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
        if event.type == pygame.MOUSEBUTTONDOWN and game_active:
            if pygame.mouse.get_pressed()[0]:
                if bullets > 0:
                    bullet_active = True
                    bullets -= 1
                    bullet.add(Bullet())
            if pygame.mouse.get_pressed()[2]:
                if bullets >= 3:
                    bullets -= 3
                    shotgun = pygame.draw.rect(screen, "Black", (playerXpos - 49, playerYpos - 100, 100, 100), border_radius=8)
                    if heart_list_index3 > 0:
                        heart_list_index3 -= 1
                        heart3 = pygame.image.load(heart_list3[heart_list_index3])
                    elif heart_list_index2 > 0:
                        heart_list_index2 -= 1
                        heart2 = pygame.image.load(heart_list2[heart_list_index2])
                    elif heart_list_index1 > 0:
                        heart_list_index1 -= 1
                        heart1 = pygame.image.load(heart_list1[heart_list_index1])

                    # if shotgun.colliderect(bullet)
                    #     print("ok")

        if not game_active:
            if event.type == animation_timer:
                if start_menu_player_list_index <= 2:
                    start_menu_player_list_index += 1
                else:
                    start_menu_player_list_index = 0
                start_menu_player = pygame.image.load(start_menu_player_list[start_menu_player_list_index])
                screen.blit(start_menu_player, start_menu_player_rect)
        if game_active:
            if event.type == bullet_spawn_timer:
                if bullets <= 4:
                    if len(spawningBullets) <= 4:
                        spawningBullets.add(SpawningBullets(randint(100, 900), randint(100, 700)))

    if game_active:

        player.update()
        player.draw(screen)

        eyes.update()
        eyes.draw(screen)

        gun.update()
        gun.draw(screen)

        spawningBullets.draw(screen)

        if bullet_active:
            bullet.update()
            bullet.draw(screen)

        enemy.update()
        enemy.draw(screen)

        sprite_collision()
        penguin_shot()

        bullet_counter_font = counter_font.render(f"Bullets: {bullets}", True, "Black")
        screen.blit(bullet_counter_font, bullet_counter_font_rect)
        screen.blit(heart1, heart1_rect)
        screen.blit(heart2, heart2_rect)
        screen.blit(heart3, heart3_rect)

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
