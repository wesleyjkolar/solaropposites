import pygame
from pygame import mixer
from pygame.locals import *
import random



pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

#define fps
clock = pygame.time.Clock()
fps = 60



screen_width = 600
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Solar Opposites')

font30 = pygame.font.SysFont('Constantia', 30)
font40 = pygame.font.SysFont('Constantia', 40)


#load sounds
explosion_fx = pygame.mixer.Sound("images/img_explosion (1).wav")
explosion_fx.set_volume(0.25)

explosion2_fx = pygame.mixer.Sound("images/img_explosion2.wav")
explosion_fx.set_volume(0.25)

laser_fx = pygame.mixer.Sound("images/img_laser.wav")
laser_fx.set_volume(0.25)

#define ame variables
rows = 4
cols = 5
goobler_cooldown = 1000
last_goobler_shot = pygame.time.get_ticks()
countdown = 3
last_count = pygame.time.get_ticks()
game_over = 0 #0 is no game over, 1 means players has won, -1 means player lost




#define colors
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)



#load img
bg = pygame.image.load("images/Untitled_Artwork.png").convert()


def draw_bg():
    screen.blit(bg, (0, 0))

#define funct for creating text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


#create korvo class
class Korvo(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/korvo.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health 
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()
    

    def update(self):
        #set move speed
        speed = 8
        #set cooldown variable
        cooldown = 500 #milliseconds
        game_over = 0


        #get key press
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += speed



#record current time
        time_now = pygame.time.get_ticks()
        #shooting
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            laser_fx.play()
            bullet = Bullets(self.rect.right - 5, self.rect.top)
            bullet_group.add(bullet) 
            self.last_shot = time_now


        #update mask
        self.mask = pygame.mask.from_surface(self.image)


    #draw healthbar
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)), 15))
        elif self.health_remaining <= 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add(explosion)
            self.kill()
            game_over = -1
        return game_over



#create bullets class
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/bullet.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
    
    def update(self):
        self.rect.y -= 5
        if self.rect.bottom <  0:
            self.kill()
        if pygame.sprite.spritecollide(self, goobler_group, True):
            self.kill()
            explosion_fx.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)

        




#create gooblers class
class Gooblers(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/goobler' + str(random.randint(1, 5)) + '.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction= 1

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction

#create goobler bullets class
class Goobler_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/goobler_bullet.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
    
    def update(self):
        self.rect.y += 2
        if self.rect.top > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self, korvo_group, False, pygame.sprite.collide_mask):
            self.kill()
            explosion2_fx.play()
            #reduce korvo health
            korvo.health_remaining -= 1
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            explosion_group.add(explosion)
          


#create explosion class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f"images/exp{num}.png")
            if size == 1:
                img = pygame.transform.scale(img, (20, 20))
            if size == 2:
                img = pygame.transform.scale(img, (40, 40))
            if size == 3:
                img = pygame.transform.scale(img, (160, 160))
            #add to list
            self.images.append(img)
        self.index = 0

        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 3
    #update explode animate
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
    #if complete delete
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()




#create sprite groups
korvo_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
goobler_group = pygame.sprite.Group()
goobler_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()

def create_gooblers():
    #generate goobs
    for row in range(rows):
        for item in range(cols):
            goobler = Gooblers(100 + item * 100, 100 + row * 70)
            goobler_group.add(goobler)

create_gooblers()






#creat player
korvo = Korvo(screen_width / 2, screen_height - 100, 3)
korvo_group.add(korvo)







run = True
while run:

    clock.tick(fps)


#draw background
    draw_bg()

    if countdown == 0:
        #create random goobler bullets
        #record current time
        time_now = pygame.time.get_ticks()
        #shoot
        if time_now - last_goobler_shot > goobler_cooldown and len(goobler_bullet_group) < 5 and len(goobler_group) > 0:
            attacking_goobler = random.choice(goobler_group.sprites())
            goobler_bullet = Goobler_Bullets(attacking_goobler.rect.centerx, attacking_goobler.rect.bottom)
            goobler_bullet_group.add(goobler_bullet)
            last_goobler_shot = time_now
    #check if all gooblers are dead
        if len(goobler_group) == 0:
            game_over = 1
            


        if game_over == 0:

        #UPDATE korvo
            game_over = korvo.update()
        


        #UPDATE SPRITE GROUPDS
            bullet_group.update()
            goobler_group.update()
            goobler_bullet_group.update()
        else: 
            if game_over == -1:
                draw_text("GET FUCKED, KORVO!", font40, white, int(screen_width / 2 - 180), int(screen_height / 2 + 50))
            if game_over == 1:
                draw_text("YOU WIN!!!!!!", font40, white, int(screen_width / 2 - 180), int(screen_height / 2 + 50))
    if countdown > 0:
        draw_text("Get Ready Korvo!", font40, white, int(screen_width / 2 - 130), int(screen_height / 2 + 50))
        draw_text(str(countdown), font30, white, int(screen_width / 2 - 10), int(screen_height / 2 + 100))
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 1000:
            countdown -= 1
            last_count = count_timer
    
    
    #update explosion group
    explosion_group.update()


    #draw sprite group
    korvo_group.draw(screen)
    bullet_group.draw(screen)
    goobler_group.draw(screen)
    goobler_bullet_group.draw(screen)
    explosion_group.draw(screen)

    #event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    

    pygame.display.update()

pygame.quit()


