import pygame as pg
from pygame import mixer
import random 
import math


# Initialize pygame
pg.init()


# Creating Screen
screen = pg.display.set_mode((800, 600))

# Background image
background = pg.image.load(".\Resources\800 x 600.jpg")


# Changing the icon
icon = pg.image.load(".\Resources\game-controller.png")
pg.display.set_icon(icon)

# Coding the player/spaceship
player_image = pg.image.load(".\Resources\spaceship.png")
player_x = 365
player_y = 480

player_x_change = 0









def player(x, y):
    screen.blit(player_image, (x, y))



# Alien spaceship

alien_img = []
alien_x = []
alien_y = []
alien_x_change = []
alien_y_change = []
num_aliens = 6
aliens = [pg.image.load(".\Resources\\alien.png"), pg.image.load(".\Resources\\rocket.png")]

for alien in range(num_aliens):
    alien_img.append(random.choice(aliens))
    alien_x.append(random.randint(0, 736))
    alien_y.append(random.randint(50, 150))
    alien_x_change.append(random.choice([-0.5, 0.5]))
    alien_y_change.append(50)


def aliens (x, y, alien):
    screen.blit(alien_img[alien], (x, y))

# Bullet

bullet_img = pg.image.load(".\Resources\\bullet.png")
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 10
bullet_state = "ready"

def fire_bullet(x, y):

    global bullet_state

    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))

# Sound
mixer.music.load(".\Resources\Sounds\\background.wav")
mixer.music.play(-1)

    

# Changing the caption
pg.display.set_caption("Space Invaders")

# Collisions
# \/----(a - b)^2 + (a - b)^2
def is_collision(alien_x,alien_y,bullet_x, bullet_y):
    
    distance = math.sqrt(math.pow(alien_x - bullet_x, 2) + math.pow(alien_y - bullet_y, 2))
    
    if distance < 20:
        return True
    
    else:
        return False

# Gameover txt

game_over = pg.image.load(".\Resources\\game_over.png")\


def game_over_text():
    global game_over

    screen.blit(game_over, (150, 25))



# Score

text_x = 10
text_y = 10

score_value = 0
font = pg.font.Font("freesansbold.ttf", 32)

def show_score(x, y):
    score = font.render(f"Score: {score_value}", True, (255, 255, 255))
    screen.blit(score, (x, y))


class Explosion(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.images = []
        for i in range(1, 6):
            img = pg.image.load(f".\Costumes\Explosion\explosion_{i}.png")
            img = pg.transform.scale(img, (100, 100))
            self.images.append(img)

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.counter = 0
        self.rect.center = [x, y]
        
    def update(self):
        explosion_speed = 10
        self.counter += 1
        
        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()

explosion_group = pg.sprite.Group()


# Game Loop
is_running = True

while is_running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))   

    explosion_group.draw(screen)
    explosion_group.update()

    




    for event in pg.event.get():
        if event.type == pg.QUIT:
            is_running = False
            

        if event.type == pg.KEYDOWN:

            if event.key == pg.K_LEFT:
                player_x_change = -0.75

            if event.key == pg.K_RIGHT:
                player_x_change = 0.75

            if event.key == pg.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound(".\Resources\Sounds\laser.wav")
                    bullet_sound.play()
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)
            



                

        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                player_x_change = 0

    player_x += player_x_change

    if player_x <= 0:
        player_x = 0

    elif player_x >= 736:
        player_x = 736

    # Aliens

    for i in range(num_aliens):

        # Gameover
        if alien_y[i] > 440:
            for j in range(num_aliens):
                alien_y[j] = 2000
                
            game_over_text()
            break



        alien_x[i] += alien_x_change[i]

        if alien_x[i] <= 0:
            alien_x_change[i] *= -1
            alien_y[i] += alien_y_change[i]

        elif alien_x[i] >= 736:
            alien_x_change[i] *= -1
            alien_y[i] += alien_y_change[i]
        
        # Bullet and enemy collision

        collsiion = is_collision(alien_x[i], alien_y[i], bullet_x, bullet_y)
        if collsiion:
            explosion = Explosion(alien_x[i], alien_y[i])
            explosion_group.add(explosion)
            explosion_sound = mixer.Sound(".\Resources\Sounds\EXPLOSION #2.wav")
            explosion_sound.play()

            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            alien_x[i] = random.randint(0, 736)
            alien_y[i] = random.randint(50, 150)
        aliens(alien_x[i], alien_y[i], i)


    # Bullet 
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change


    player(player_x, player_y)

    show_score(text_x, text_y)

    pg.display.update()
