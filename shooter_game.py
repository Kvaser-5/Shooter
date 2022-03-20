from pygame import *
from random import randint
 

mixer.init()
mixer.music.load('dominirovanie-igrovogo-personaja-po-vneshnemu-vidu-bgm-42277.mp3')
mixer.music.play()
fire_sound = mixer.Sound('scifi-film-lazernaya-pushka-zvukovyie-effektyi-43061.ogg')
 

img_back = "maxresdefault.jpg" 
img_hero = "kisspng-serious-sam-3-bfe-serious-sam-hd-the-second-enco-5ae4d54060c033.2214879315249462403963.png"
img_bullet = "bullet.png" 
img_enemy = "kisspng-clops-clops-skeleton-bone-insect-deviantart-5b2c67a6630cc7.4214597715296367744057.png"
score = 0
goal = 10
max_lost = 3
lost = 0 

class GameSprite(sprite.Sprite):
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       
       sprite.Sprite.__init__(self)
 
       
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
 
       
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
 

class Player(GameSprite):
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed

   def fire(self):
       bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, 15)
       bullets.add(bullet)
 
 
class Enemy(GameSprite):
   def update(self):
       self.rect.y += self.speed
       global lost

       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0
           lost = lost + 1
 
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
 
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
   monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
   monsters.add(monster)
 
bullets = sprite.Group()

FPS = 60
finish = False
run = True
font.init()
font1 = font.Font(None, 80)

font2 = font.Font(None, 36)

while run:
   for e in event.get():
        if e.type == QUIT:
           run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()

   if not finish:
        window.blit(background,(0,0))

        ship.update()
        monsters.update()
        bullets.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        lose = font1.render('YOU LOSE!', 3, (255, 255, 255))
        win = font2.render('YOU WIN!', 3, (255, 255, 255))

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
           score = score + 1
           monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
           monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
 

        display.update()
        time.delay(50)



