from pygame import *
from random import randint, choice
from time import sleep

def lose_condition():
    for enemy in Enemy.enemies:
        if enemy.rect.y >= 720:
            enemy.kill()
            return True


win = display.set_mode((1080, 720))
display.set_caption('Space Invaders')
display.set_icon(transform.scale(image.load('images/spaceship.png'), (32, 32)))
background1 = transform.scale(image.load('images/backgroung.png'), (1080, 720))
win.blit(background1, (0, 0))

class Sprite(sprite.Sprite):
    def __init__(self, w, h, x, y, file_name):
        super().__init__()
        self.image = transform.scale(image.load(file_name), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player(Sprite):
    def __init__(self, w, h, x, y, filename, speed=5):
        super().__init__(w, h, x, y, filename)
        self.speed = speed

    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 980:
            self.rect.x += self.speed

    def shoot(self):
        Bullet(10, 10, self.rect.centerx - 5, self.rect.top, 'images/bullet.png')

class Enemy(Sprite):
    enemies = sprite.Group()
    def __init__(self, w, h, x, y, filename, speed=5):
        super().__init__(w, h, x, y, filename)
        self.speed = speed
        self.direction = choice(['left', 'right'])
        Enemy.enemies.add(self)

    def update(self):
        self.rect.y += self.speed
        if self.speed < 2:
            if self.direction == 'right':
                self.rect.x += self.speed
                if self.rect.x > 980:
                    self.direction = 'left'
            else:
                self.rect.x -= self.speed
                if self.rect.x < 0:
                    self.direction = 'right'



class Bullet(Sprite):
    bullets = sprite.Group()
    def __init__(self, w, h, x, y, filename, speed=5):
        super().__init__(w, h, x, y, filename)
        self.speed = speed
        Bullet.bullets.add(self)

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -25:
            self.kill()

rocket = Player(100, 130, 500, 500, 'images/rocket.png')
button = Sprite(200, 100, 450, 500, 'images/restart.png')


mixer.init()
mixer.music.load('game_music.wav')
mixer.music.play(-1)
mixer.music.set_volume(0.1)
fail_sound = mixer.Sound('collision_sound.wav')


clock = time.Clock()

heart1 = transform.scale(image.load('images/Heart1.png'), (70, 70))
heart2 = transform.scale(image.load('images/Heart2.png'), (70, 70))
one = transform.scale(image.load('images/one.png'), (80, 80))
two = transform.scale(image.load('images/two.png'), (100, 100))
three = transform.scale(image.load('images/three.png'), (100, 100))

# 97
lifes = 3


finish = True
button.draw()
counter = 0
while True:
    if not finish:
        win.blit(background1, (0, 0))
        rocket.draw()
        rocket.update()
        Bullet.bullets.draw(win)
        Bullet.bullets.update()

        if len(Enemy.enemies) == 0:
            for i in range(5):
                x = randint(0, 980)
                speed = randint(1, 2)
                Enemy(100, 40, x, -100, 'images/spaceship.png', speed)
            counter += 1
        Enemy.enemies.draw(win)
        Enemy.enemies.update()

        sprite.groupcollide(Enemy.enemies, Bullet.bullets, True, True)

        x = 870
        for i in range(3):
            win.blit(heart2, (x, 0))
            x += 70

        x = 870
        for i in range(lifes):
            win.blit(heart1, (x, 0))
            x += 70

        if sprite.spritecollide(rocket, Enemy.enemies, True) or lose_condition():
            lifes -= 1
            fail_sound.play()
            if lifes == 0:
                button.rect.x = 450
                game_over = transform.scale(image.load('images/game_over.png'), (1080, 720))
                win.blit(game_over, (0, 0))
                mixer.music.stop()
                mixer.music.load('game_over.wav')
                mixer.music.set_volume(0.5)
                mixer.music.play()
                finish = True
                button.draw()

        if counter > 3:
            button.rect.x = 450
            winner = transform.scale(image.load('images/winner.png'), (1080, 720))
            win.blit(winner, (0, 0))
            mixer.music.stop()
            mixer.music.load('winner.wav')
            mixer.music.set_volume(0.5)
            mixer.music.play()
            finish = True
            button.draw()

    for e in event.get():
        if e.type == KEYDOWN and e.key == K_SPACE:
            rocket.shoot()
        if e.type == QUIT:
            quit()
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            x, y = mouse.get_pos()
            if button.rect.collidepoint(x, y):
                button.rect.x = -300
                win.blit(background1, (0, 0))
                win.blit(three, (500, 500))
                display.update()
                sleep(0.5)
                win.blit(background1, (0, 0))
                win.blit(two, (500, 500))
                display.update()
                sleep(0.5)
                win.blit(background1, (0, 0))
                win.blit(one, (500, 500))
                display.update()
                sleep(0.5)
                finish = False
                lifes = 3
                counter = 0
                Enemy.enemies.empty()
                mixer.music.load('game_music.wav')
                mixer.music.set_volume(0.1)
                mixer.music.play(-1)

    display.update()
    clock.tick(60)
