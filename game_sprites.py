import os
import random
import pygame
from conf import HEIGHT, WIDTH, BOTTOM, TOP, BLACK

if pygame.get_init() is False:
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sarah's Dream")
    clock = pygame.time.Clock()
    font_name = pygame.font.match_font("arial")

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")
bg_folder = os.path.join(img_folder, "bg")
orbs_folder = os.path.join(img_folder, "orbs")
players_folder = os.path.join(img_folder, "players")
bonus_folder = os.path.join(img_folder, "bonus")
enemies_folder = os.path.join(img_folder, "enemies")
explosions_folder = os.path.join(img_folder, "explosions")
orb_img = os.path.join(orbs_folder, "orb.png")

player_img = pygame.image.load(os.path.join(players_folder, "sarah.png")).convert_alpha()
pow1_img = pygame.image.load(os.path.join(bonus_folder, "pow1.png")).convert()
pow2_img = pygame.image.load(os.path.join(bonus_folder, "pow2.png")).convert()
bonus_img = {}
bonus_img["life"] = pygame.transform.scale(player_img, (20, 32))
bonus_img["power"] = {}
bonus_img["power"]["sm"] = pygame.transform.scale(pow1_img, (32, 32))
bonus_img["power"]["lg"] = pygame.transform.scale(pow2_img, (32, 32))

suicaman_img = pygame.image.load(os.path.join(enemies_folder, "suicaman.png")).convert_alpha()
suicaman_img = pygame.transform.scale(suicaman_img, (100, 100))
suica_seed_img = pygame.image.load(os.path.join(enemies_folder, "suica_seed.png")).convert_alpha()

pampa_img = pygame.image.load(os.path.join(enemies_folder, "pampa.png")).convert_alpha()
pampa_img = pygame.transform.scale(pampa_img, (110, 85))

boss_lvl1_img = pygame.image.load(os.path.join(enemies_folder, "boss_lvl1.png")).convert_alpha()
boss_lvl1_img = pygame.transform.scale(boss_lvl1_img, (235, 200))
boss_lvl1_img_2 = pygame.image.load(os.path.join(enemies_folder, "boss_lvl1_2.png")).convert_alpha()
boss_lvl1_img_2 = pygame.transform.scale(boss_lvl1_img_2, (235, 200))
boss_lvl1_img_3 = pygame.image.load(os.path.join(enemies_folder, "boss_lvl1_3.png")).convert_alpha()
boss_lvl1_img_3 = pygame.transform.scale(boss_lvl1_img_3, (235, 200))
boss_lvl1_atk1 = pygame.image.load(os.path.join(enemies_folder, "boss_atk1.png")).convert_alpha()
boss_lvl1_atk2 = pygame.image.load(os.path.join(enemies_folder, "boss_atk2.png")).convert_alpha()
boss_lvl1_atk3 = pygame.image.load(os.path.join(enemies_folder, "boss_atk3.png")).convert_alpha()


boss_lvl2_img = pygame.image.load(os.path.join(enemies_folder, "boss_lvl2.png")).convert_alpha()
boss_lvl2_img = pygame.transform.scale(boss_lvl2_img, (200, 200))
boss_lvl2_img_2 = pygame.image.load(os.path.join(enemies_folder, "boss_lvl2_2.png")).convert_alpha()
boss_lvl2_img_2 = pygame.transform.scale(boss_lvl2_img_2, (200, 200))
boss_lvl2_img_3 = pygame.image.load(os.path.join(enemies_folder, "boss_lvl2_2.png")).convert_alpha()
boss_lvl2_img_3 = pygame.transform.scale(boss_lvl2_img_3, (200, 200))

dragons_img = []
dragons = ["dragon1.png", "dragon2.png", "dragon3.png"]
for dragon in dragons:
    dragons_img.append(pygame.image.load(os.path.join(enemies_folder, dragon)).convert())

fireball_image = pygame.image.load(os.path.join(enemies_folder, "fireball.png")).convert()

bee_img = pygame.image.load(os.path.join(enemies_folder, "bee.png")).convert_alpha()
bee_img = pygame.transform.scale(bee_img, (100, 125))
bee_needle_img = pygame.image.load(os.path.join(enemies_folder, "bee_needle.png")).convert_alpha()

explosion_anim = {}
explosion_anim["lg"] = []
explosion_anim["sm"] = []
explosion_anim["player"] = []
for i in range(9):
    filename = "regularExplosion0{}.png".format(i)
    img = pygame.image.load(os.path.join(explosions_folder, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim["lg"].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim["sm"].append(img_sm)
    filename = "sonicExplosion0{}.png".format(i)
    img = pygame.image.load(os.path.join(explosions_folder, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim["player"].append(img)


class SpriteGroups:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.dragons = pygame.sprite.Group()
        self.suicamans = pygame.sprite.Group()
        self.pampas = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.bosses = pygame.sprite.Group()
        self.orbs = pygame.sprite.Group()
        self.fireballs = pygame.sprite.Group()
        self.bees = pygame.sprite.Group()
        self.needles = pygame.sprite.Group()
        self.seeds = pygame.sprite.Group()
        self.bombs_lvl1 = pygame.sprite.Group()
        self.bonus = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    def __init__(self, sprite_groups, player_width=65, player_height=75):
        pygame.sprite.Sprite.__init__(self)
        self.type = "player"
        self.image = pygame.transform.scale(player_img, (player_width, player_height))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = 100
        self.rect.centery = HEIGHT / 2
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.last_hitted = pygame.time.get_ticks()
        self.power = 3  # 0
        self.speedx = 0
        self.speedy = 0
        self.lives = 99  # 3
        self.radius = 20
        self.score = 0
        self.dragon_killed = 0
        self.pampa_killed = 0
        self.bee_killed = 0
        self.suicaman_killed = 0
        self.pampas_summoned = False
        self.boss_lvl1_summoned = False
        self.boss_lvl1_defeated = False
        self.boss_lvl2_summoned = False
        self.boss_lvl2_defeated = False
        self.sprite_groups = sprite_groups
        self.sprite_groups.players.add(self)
        self.sprite_groups.all_sprites.add(self)

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_UP]:
            self.speedy = -8
        if keystate[pygame.K_DOWN]:
            self.speedy = 8
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power >= 0:
                orb = Orb(self.rect.right + 20, self.rect.centery - 10, "pow0")
                self.sprite_groups.all_sprites.add(orb)
                self.sprite_groups.orbs.add(orb)
            if self.power >= 1:
                orb = Orb(self.rect.right + 20, self.rect.centery - 10, "pow1")
                self.sprite_groups.all_sprites.add(orb)
                self.sprite_groups.orbs.add(orb)
            if self.power >= 2:
                orb = Orb(self.rect.right + 20, self.rect.centery - 10, "pow2")
                self.sprite_groups.all_sprites.add(orb)
                self.sprite_groups.orbs.add(orb)


class Orb(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.orb_img = pygame.image.load(orb_img).convert()
        self.image_orig = self.orb_img
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.centery = y
        self.rect.centerx = x
        self.rect.right = x
        self.type = type
        if self.type == "pow0":
            self.speedy = 0
        if self.type == "pow1":
            self.speedy = 2
        if self.type == "pow2":
            self.speedy = -2
        self.speedx = 8
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()
        self.hit_time = None

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # If the orb reach the right edge of the screen, delete it
        if self.rect.right > WIDTH:
            self.kill()


class Dragon(pygame.sprite.Sprite):
    def __init__(self, sprite_groups):
        pygame.sprite.Sprite.__init__(self)
        self.type = "enemy"
        self.image = random.choice(dragons_img)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = random.randrange(100, HEIGHT - 100)
        self.speedx = -4
        self.speedy = 0
        self.last_hit = pygame.time.get_ticks()
        self.untouchable_time = 1000
        self.shoot_delay = 500
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.sprite_groups = sprite_groups

    def update(self):
        self.shoot()
        if self.rect.x > WIDTH - 200:
            self.rect.x += self.speedx

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            fireball = Fireball(self.rect.x + 50, self.rect.y)
            self.sprite_groups.all_sprites.add(fireball)
            self.sprite_groups.fireballs.add(fireball)
            self.sprite_groups.enemies.add(fireball)


class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.type = "enemy"
        self.image_orig = pygame.transform.scale(fireball_image, (24, 22))
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        self.rect.y = y
        self.rect.x = x
        self.rect.right = x
        self.speedx = -8
        self.speedy = random.randrange(-2, 2)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # If the orb reach the left edge of the screen, delete it
        if self.rect.right < 0:
            self.kill()


class Bee(pygame.sprite.Sprite):
    def __init__(self, sprite_groups):
        pygame.sprite.Sprite.__init__(self)
        self.type = "enemy"
        self.image = bee_img
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = (HEIGHT - self.rect.height) / 2
        self.go_to = random.choice([BOTTOM, TOP])
        self.speedx = -4
        self.last_hit = pygame.time.get_ticks()
        self.untouchable_time = 1000
        self.shoot_delay = 500
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.sprite_groups = sprite_groups

    def update(self):
        self.shoot()
        if self.rect.x > WIDTH - 200:
            self.rect.x += self.speedx
        else:
            if self.go_to == BOTTOM:
                self.rect.y += 4
                if self.rect.y >= BOTTOM:
                    self.go_to = TOP
            elif self.go_to == TOP:
                self.rect.y += -4
                if self.rect.y <= 0:
                    self.go_to = BOTTOM

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            needle = Needle(self.rect.x + 50, self.rect.y + 50)
            self.sprite_groups.all_sprites.add(needle)
            self.sprite_groups.needles.add(needle)
            self.sprite_groups.enemies.add(needle)


class Needle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.type = "enemy"
        self.image = pygame.transform.scale(bee_needle_img, (24, 22))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        self.rect.y = y
        self.rect.x = x
        self.rect.right = x
        self.speedx = -8
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.speedx
        # If the orb reach the left edge of the screen, delete it
        if self.rect.right < 0:
            self.kill()


class Suicaman(pygame.sprite.Sprite):
    def __init__(self, sprite_groups):
        pygame.sprite.Sprite.__init__(self)
        self.type = "enemy"
        self.image = suicaman_img
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = random.randrange(100, HEIGHT - 100)
        self.radius = int(self.rect.width * .75 / 2)
        self.speedx = -4
        self.last_hit = pygame.time.get_ticks()
        self.untouchable_time = 1000
        self.shoot_delay = 1000
        self.last_shot = pygame.time.get_ticks()
        self.lives = 2
        self.sprite_groups = sprite_groups

    def update(self):
        self.shoot()
        if self.rect.x > WIDTH - 200:
            self.rect.x += self.speedx

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            seed = Seed(self.rect.x + 50, self.rect.y + 50)
            self.sprite_groups.all_sprites.add(seed)
            self.sprite_groups.seeds.add(seed)
            self.sprite_groups.enemies.add(seed)


class Seed(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.type = "enemy"
        self.image = pygame.transform.scale(suica_seed_img, (30, 19))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        self.rect.y = y
        self.original_y = y
        self.rect.x = x
        self.rect.right = x
        self.speedx = -4
        self.last_update = pygame.time.get_ticks()
        self.direction = "neutral"

    def update(self):
        self.rect.x += self.speedx
        # If the orb reach the left edge of the screen, delete it
        if self.rect.right < 0:
            self.kill()
        # wave attack
        if self.original_y - self.rect.y <= 64 and self.direction != "bot":
            self.rect.y -= 2
            self.direction = "top"
        elif self.original_y - self.rect.y > 64 or self.direction == "bot":
            self.rect.y += 2
            self.direction = "bot"
            if self.original_y - self.rect.y <= -64:
                self.direction = "top"


class Pampa(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.type = "enemy"
        self.image = pampa_img
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = WIDTH
        self.rect.y = random.randrange(100, HEIGHT - 100)
        self.speedx = random.randrange(3, 8)
        self.speedy = random.randrange(-3, 3)
        self.last_update = pygame.time.get_ticks()
        self.lives = 1

    def update(self):
        self.rect.x -= self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -100 or self.rect.bottom < -10:
            self.rect.x = WIDTH
            self.rect.y = random.randrange(100, HEIGHT - 100)
            self.speedx = random.randrange(1, 8)
            self.speedy = random.randrange(-3, 3)


class Boss_lvl1(pygame.sprite.Sprite):
    def __init__(self, sprite_groups):
        pygame.sprite.Sprite.__init__(self)
        self.type = "enemy"
        self.image = boss_lvl1_img
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = (HEIGHT - self.rect.height) / 2
        self.radius = int(self.rect.width * .75 / 2)
        self.speedx = -4
        self.speedy = random.randrange(-3, 3)
        self.lives = 21
        self.last_hit = pygame.time.get_ticks()
        self.untouchable_time = 1500
        self.shoot_delay = 1000
        self.last_shot = pygame.time.get_ticks()
        self.sprite_groups = sprite_groups

    def update(self):
        self.shoot()
        if self.rect.x > WIDTH - 200:
            self.rect.x += self.speedx
        if 7 < self.lives < 15:
            self.image = boss_lvl1_img_2
        if 0 < self.lives < 8:
            self.image = boss_lvl1_img_3

    def shoot(self):
        if 7 < self.lives < 15:
            bullet_lvl = 2
        elif 0 < self.lives < 8:
            bullet_lvl = 3
        else:
            bullet_lvl = 1
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bomb = Bomb_lvl1(self.rect.x + 50, self.rect.y + 50, bullet_lvl, self.sprite_groups)
            self.sprite_groups.all_sprites.add(bomb)
            self.sprite_groups.bombs_lvl1.add(bomb)
            self.sprite_groups.enemies.add(bomb)



class Bomb_lvl1(pygame.sprite.Sprite):
    def __init__(self, x, y, lvl, sprite_groups):
        pygame.sprite.Sprite.__init__(self)
        self.type = "enemy"
        self.lvl = lvl
        if lvl == 1:
            self.bullet_image = boss_lvl1_atk1
        elif lvl == 2:
            self.bullet_image = boss_lvl1_atk2
        elif lvl == 3:
            self.bullet_image = boss_lvl1_atk3
        self.image = pygame.transform.scale(self.bullet_image, (32, 33))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        self.rect.y = y
        self.rect.x = x
        self.rect.right = x
        self.speedx = -8
        self.exp_x = random.randrange(0, WIDTH - 300)
        self.last_update = pygame.time.get_ticks()
        self.sprite_groups = sprite_groups

    def update(self):
        self.rect.x += self.speedx
        # If the orb reach the left edge of the screen, delete it
        if self.rect.x < 0:
            self.kill()
        if self.rect.right < self.exp_x:
            if self.lvl == 1:
                for i in range(4):
                    bomb_exp = Bomb_Exp(self.rect.x, self.rect.y, i, self.bullet_image, self.lvl)
                    self.sprite_groups.all_sprites.add(bomb_exp)
                    self.sprite_groups.bombs_lvl1.add(bomb_exp)
                    self.sprite_groups.enemies.add(bomb_exp)
            if self.lvl == 2:
                for i in range(8):
                    bomb_exp = Bomb_Exp(self.rect.x, self.rect.y, i, self.bullet_image, self.lvl)
                    self.sprite_groups.all_sprites.add(bomb_exp)
                    self.sprite_groups.bombs_lvl1.add(bomb_exp)
                    self.sprite_groups.enemies.add(bomb_exp)
            if self.lvl == 3:
                for i in range(12):
                    bomb_exp = Bomb_Exp(self.rect.x, self.rect.y, i, self.bullet_image, self.lvl)
                    self.sprite_groups.all_sprites.add(bomb_exp)
                    self.sprite_groups.bombs_lvl1.add(bomb_exp)
                    self.sprite_groups.enemies.add(bomb_exp)
            self.kill()



class Bomb_Exp(pygame.sprite.Sprite):
    def __init__(self, x, y, n, bullet_image, lvl):
        pygame.sprite.Sprite.__init__(self)
        self.type = "enemy"
        self.image = pygame.transform.scale(bullet_image, (24, 25))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        self.rect.y = y
        if lvl == 1:
            if n == 0:
                self.rot = 45
                self.speedx = -2
                self.speedy = 2
            if n == 1:
                self.rot = 135
                self.speedx = 2
                self.speedy = 2
            if n == 2:
                self.rot = 225
                self.speedx = 2
                self.speedy = -2
            if n == 3:
                self.rot = 315
                self.speedx = -2
                self.speedy = -2
        elif lvl == 2:
            if n == 0:
                self.rot = 0
                self.speedx = -4
                self.speedy = 0
            if n == 1:
                self.rot = 45
                self.speedx = -2
                self.speedy = 2
            if n == 2:
                self.rot = 90
                self.speedx = 0
                self.speedy = 4
            if n == 3:
                self.rot = 135
                self.speedx = 2
                self.speedy = 2
            if n == 4:
                self.rot = 180
                self.speedx = 4
                self.speedy = 0
            if n == 5:
                self.rot = 225
                self.speedx = 2
                self.speedy = -2
            if n == 6:
                self.rot = 270
                self.speedx = 0
                self.speedy = -4
            if n == 7:
                self.rot = 315
                self.speedx = -2
                self.speedy = -2
        elif lvl == 3:
            if n == 0:
                self.rot = 0
                self.speedx = -3
                self.speedy = 0
            if n == 1:
                self.rot = 30
                self.speedx = -2
                self.speedy = 1
            if n == 2:
                self.rot = 60
                self.speedx = -1
                self.speedy = 2
            if n == 3:
                self.rot = 90
                self.speedx = 0
                self.speedy = 3
            if n == 4:
                self.rot = 120
                self.speedx = 1
                self.speedy = 2
            if n == 5:
                self.rot = 150
                self.speedx = 2
                self.speedy = 1
            if n == 6:
                self.rot = 180
                self.speedx = 3
                self.speedy = 0
            if n == 7:
                self.rot = 210
                self.speedx = 2
                self.speedy = -1
            if n == 8:
                self.rot = 240
                self.speedx = 1
                self.speedy = -2
            if n == 9:
                self.rot = 270
                self.speedx = 0
                self.speedy = -3
            if n == 10:
                self.rot = 300
                self.speedx = -1
                self.speedy = -2
            if n == 11:
                self.rot = 330
                self.speedx = -2
                self.speedy = -1
            if n == 12:
                self.rot = 360
                self.speedx = -3
                self.speedy = 0
        new_image = pygame.transform.rotate(self.image, self.rot)
        old_center = self.rect.center
        self.image = new_image
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        self.rect.x = x
        self.rect.right = x
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # If the orb reach the left edge of the screen, delete it
        if self.rect.right < 0:
            self.kill()


class Bonus(pygame.sprite.Sprite):
    def __init__(self, center, player):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(["life", "power"])
        self.image = bonus_img[self.type]
        if self.type == "power" and player.power == 0:
            self.image = bonus_img[self.type]["sm"]
        elif self.type == "power" and player.power >= 1:
            self.image = bonus_img[self.type]["lg"]
        #self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedx = -3

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += random.randrange(-2, 2)
        # kill if it moves off the top of the screen
        if self.rect.right < 0:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.type = "explosion"
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
