import pygame
from pygame.constants import K_RIGHT
import random
import os

#variables
FPS = 60 

# Dimensions
WIDTH = 500
HEIGHT = 600

#colours
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)

# setting the window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Testing")
clock = pygame.time.Clock()

#Images
background_img = pygame.image.load(os.path.join("Image", "background1.jpeg")).convert()
bullet_img = pygame.image.load(os.path.join("Image", "bullet.png")).convert()
player_img = pygame.image.load(os.path.join("Image", "x-wing.png")).convert()
#rock_img = pygame.image.load(os.path.join("Image", "rock.png")).convert()
rock_imgs = []
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join("Image", f"rock{i}.png")).convert())
font_name = pygame.font.match_font("arial")

# music 
shoot_sound = pygame.mixer.Sound(os.path.join("Sound", "shoot.wav"))
expl_sounds = [pygame.mixer.Sound(os.path.join("Sound", "expl0.wav")), pygame.mixer.Sound(os.path.join("Sound", "expl1.wav"))]
for i in range(1):
    expl_sounds[i].set_volume(0.5)
shoot_sound.set_volume(0.5)

pygame.mixer.music.load(os.path.join("Sound", "background.ogg"))

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x , y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x,y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def new_rock():
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)

# Player sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (79,81))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 8
        self.health = 100

    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0 
    #generate bullet sprite
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

# rock sprite 
class Rock(pygame.sprite.Sprite):  
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(rock_imgs)
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        #pygame.draw.circle(self.image_ori,RED,self.rect.center,self.radius)
        self.rect.x = random.randrange(0,WIDTH - self.rect.width)
        self.rect.y = random.randrange(-180,-100)
        self.speedy = random.randrange(2,10)
        self.speedx = random.randrange(-3,3)
        self.total_degree = 0
        self.rot_degree = random.randrange(-3,3)
        
        
    def rotate(self):
        self.total_degree += self.rot_degree
        #self.total_degree = self.rot_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
        
        
        

    def update(self):
       self.rotate()
       self.rect.y += self.speedy
       self.rect.x += self.speedx
       if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0,WIDTH - self.rect.width)
            self.rect.y = random.randrange(-180,-100)
            self.speedy = random.randrange(2,10)
            self.speedx = random.randrange(-3,3)
            self.rot_degree = random.randrange(-3,3)

# bullet spirte 
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.speedy = -10
        

    def update(self):
       self.rect.y += self.speedy
       if self.rect.bottom < 0:
           self.kill()


# adding all sprites in game to all_sprites
all_sprites = pygame.sprite.Group()

# group for rocks
rocks = pygame.sprite.Group()

# group for bullets
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
rock = Rock()
all_sprites.add(rock)
for i in range(8):
    new_rock()

#score
score = 0

running = True
pygame.mixer.music.play(-1)


print(pygame.sprite.Group.sprites(rocks))
# Display on  screen     
while running:
    #FPS
    clock.tick(FPS)
    #input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    #update
    all_sprites.update() 
    hits = pygame.sprite.groupcollide(rocks,bullets, True, True)
    for hit in hits:
        random.choice(expl_sounds).play()
        score += hit.radius
        new_rock()
        

    
    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.health -= hit.radius
        new_rock()
        if player.health <= 0:
            running = False
    
    # screen display
    screen.fill((BLACK))
    screen.blit(background_img, (0,0))
    all_sprites.draw(screen)  
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    draw_health(screen, player.health,10,15)
    pygame.display.update() 


pygame.quit() 