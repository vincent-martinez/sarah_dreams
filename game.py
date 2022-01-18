import pygame
import os
from conf import HEIGHT, WIDTH, BLACK, FPS, WHITE
import game_sprites
from game_collisions import check_hit_by_enemies, check_hit_bonus, check_orbs_hit_dragons, \
    check_orbs_hit_bees, check_orbs_hit_suicamans, check_orbs_hit_pampas, check_orbs_hit_boss_lvl1


# initialize pygame and create window
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
players_folder = os.path.join(img_folder, "players")

player_img = pygame.image.load(os.path.join(players_folder, "sarah.png")).convert_alpha()
player_mini_img = pygame.transform.scale(player_img, (25, 29))
player_mini_img.set_colorkey(BLACK)

sarah_dream_img = pygame.image.load(os.path.join(bg_folder, "dreaming.jpg")).convert()
sarah_dream_img = pygame.transform.scale(sarah_dream_img, (200, 266))

level_bg = {
    "level2": {
        "bg1": pygame.image.load(os.path.join(bg_folder, "level1.png"))
            .convert(),
        "bg2": pygame.image.load(os.path.join(bg_folder, "level1-2.png")).convert(),
        "bg3": pygame.image.load(os.path.join(bg_folder, "level1.png")).convert(),
    },
    "level1": {
        "bg1": pygame.image.load(os.path.join(bg_folder, "level2.png")).convert(),
        "bg2": pygame.image.load(os.path.join(bg_folder, "level2-2.png")).convert(),
        "bg3": pygame.image.load(os.path.join(bg_folder, "level2.png")).convert(),
    },
    "level3": {
        "bg1": pygame.image.load(os.path.join(bg_folder, "level3.png")).convert(),
        "bg2": pygame.image.load(os.path.join(bg_folder, "level3-2.png")).convert(),
        "bg3": pygame.image.load(os.path.join(bg_folder, "level3.png")).convert(),
    }
}
bg_x = WIDTH
transition_bg = pygame.image.load(os.path.join(bg_folder, "black.png")).convert()


def show_go_screen(saved_score, demo_end):
    global level
    gameover = saved_score
    start_screen_time = pygame.time.get_ticks()
    bg1 = level_bg["level1"]["bg1"]
    screen.blit(bg1, bg1.get_rect())
    screen.blit(sarah_dream_img, (WIDTH / 2 - 100, 120))

    if demo_end or gameover is not None:
        level = 1
        draw_text(screen, "Dream is Over", 64, WIDTH / 2, 50)
        draw_text(screen, "Score reached: %s" % saved_score, 18, WIDTH / 2, 400)
        draw_text(screen, "Press any key to start a new game", 18, WIDTH / 2, 500)
    else:
        draw_text(screen, "Sarah's Dream", 64, WIDTH / 2, 50)
        draw_text(screen, "Move the character by pressing the directional keys", 18, WIDTH / 2, 400)
        draw_text(screen, "Shoot orbs by pressing the space bar", 18, WIDTH / 2, 430)
        draw_text(screen, "You have 3 lives to defeat the monsters", 18, WIDTH / 2, 450)
        draw_text(screen, "Press any key to start a game", 18, WIDTH / 2, 550)

    if demo_end:
        draw_text(screen, "Maybe dream will be longer in the future", 18, WIDTH / 2, 550)

    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            pressed_key_time = pygame.time.get_ticks()
            if event.type == pygame.QUIT:
                pygame.quit()
            # Add security to not leave the game over screen too early
            if event.type == pygame.KEYUP and pressed_key_time - start_screen_time > 1000:
                waiting = False


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_lives(surf, x, y, lives, img):
    for l in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * l
        img_rect.y = y
        surf.blit(img, img_rect)


def new_bee(sprite_groups):
    nb = game_sprites.Bee(sprite_groups)
    sprite_groups.all_sprites.add(nb)
    sprite_groups.bees.add(nb)
    sprite_groups.enemies.add(nb)


def new_suicaman(sprite_groups):
    ns = game_sprites.Suicaman(sprite_groups)
    sprite_groups.all_sprites.add(ns)
    sprite_groups.suicamans.add(ns)
    sprite_groups.enemies.add(ns)


def summon_boss_lvl1(sprite_groups):
    global running
    boss_incoming = True
    while boss_incoming:
        clock.tick(FPS)
        for event in pygame.event.get():
            # Stop the game when window is closed
            if event.type == pygame.QUIT:
                running = False
        sprite_groups.all_sprites.update()
        scroll_background()
        sprite_groups.all_sprites.draw(screen)
        pygame.display.flip()
        now_t = pygame.time.get_ticks()
        if now_t - boss_lvl1_incoming_time > 3000:
            boss = game_sprites.Boss_lvl1(sprite_groups)
            sprite_groups.all_sprites.add(boss)
            sprite_groups.bosses.add(boss)
            sprite_groups.enemies.add(boss)
            boss_incoming = False


def start_level1(sprite_groups):
    for d in range(2):
        new_suicaman(sprite_groups)


def start_level2(sprite_groups):
    global bg_x
    global level
    global running
    boss_lvl1_killed_time = pygame.time.get_ticks()
    waiting_lvl2 = True
    while waiting_lvl2:
        clock.tick(FPS)
        for event in pygame.event.get():
            # Stop the game when window is closed
            if event.type == pygame.QUIT:
                running = False
        sprite_groups.all_sprites.update()
        scroll_background()
        sprite_groups.all_sprites.draw(screen)
        pygame.display.flip()
        now_t = pygame.time.get_ticks()
        if now_t - boss_lvl1_killed_time > 3000:
            waiting_lvl2 = False
            display_transition_screen("level 2", sprite_groups)
            waiting = True
            while waiting:
                clock.tick(FPS)
                now_t2 = pygame.time.get_ticks()
                if now_t2 - end_level1_time > 6000:
                    bg_x = WIDTH
                    level = 2
                    for d in range(2):
                        new_bee(sprite_groups)
                    waiting = False


def display_transition_screen(level, sprite_groups):
    clear_sprites(sprite_groups)
    screen.blit(transition_bg, transition_bg.get_rect())
    draw_text(screen, level, 64, WIDTH / 2, 100)
    pygame.display.flip()


def scroll_background():
    global bg_x
    bg1 = level_bg["level" + str(level)]["bg1"]
    bg2 = level_bg["level" + str(level)]["bg2"]
    bg3 = level_bg["level" + str(level)]["bg3"]
    # Draw scrollable backgrounds
    screen.blit(bg1, (bg_x, 0))
    screen.blit(bg2, (bg_x - WIDTH, 0))
    screen.blit(bg3, (bg_x - WIDTH * 2, 0))
    # Scroll backgrounds from right to left
    bg_x -= 1
    if bg_x == 0:
        bg_x = WIDTH * 2


def clear_sprites(sprite_groups):
    for s in sprite_groups.all_sprites:
        if not s.type == "player":
            s.kill()


def reset_stats(player):
    player.suicaman_killed = 0
    player.bee_killed = 0
    player.dragon_killed = 0
    player.pampa_killed = 0
    player.pampas_summoned = False
    player.boss_lvl1_summoned = False
    player.boss_lvl1_defeated = False
    player.boss_lvl2_summoned = False
    player.boss_lvl2_defeated = False


saved_score = None
player = None
start_game = True
running = True
pampas_summoned = False
boss_lvl_summoned = False
level = 1
dead_time = None
game_over = False
demo_end = False

while running:
    now = pygame.time.get_ticks()
    end_game = game_over and dead_time is not None and now - dead_time > 500
    if start_game or end_game:
        if player:
            saved_score = player.score
            reset_stats(player)
        show_go_screen(saved_score, demo_end)
        game_over = False
        demo_end = False
        start_game = False
        sprite_groups = game_sprites.SpriteGroups()
        start_level1(sprite_groups)
        player = game_sprites.Player(sprite_groups)

    # keep loop running at the right speed
    clock.tick(FPS)

    for event in pygame.event.get():
        # Stop the game when window is closed
        if event.type == pygame.QUIT:
            running = False

    sprite_groups.all_sprites.update()
    ################################
    #       Manage collisions      #
    ################################
    check_hit_by_enemies(sprite_groups, player)
    if player.lives <= 0 and not game_over:
        game_over = True
        dead_time = pygame.time.get_ticks()

    check_hit_bonus(sprite_groups, player)

    check_orbs_hit_dragons(sprite_groups, player)
    check_orbs_hit_bees(sprite_groups, player)
    check_orbs_hit_suicamans(sprite_groups, player)
    check_orbs_hit_pampas(sprite_groups, player)
    check_orbs_hit_boss_lvl1(sprite_groups, player)

    # level 1 boss summon after defeating all pampas
    if player.pampas_summoned and len(sprite_groups.pampas.sprites()) == 0 and not boss_lvl_summoned:
        boss_lvl_summoned = True
        boss_lvl1_incoming_time = pygame.time.get_ticks()
        summon_boss_lvl1(sprite_groups)
    # go to level 2
    if level == 1 and player.boss_lvl1_defeated:
        end_level1_time = pygame.time.get_ticks()
        start_level2(sprite_groups)

    # TODO: finish game
    if player.dragon_killed >= 10:
        demo_end = True
        game_over = True
        dead_time = pygame.time.get_ticks()

    scroll_background()
    sprite_groups.all_sprites.draw(screen)
    draw_text(screen, str(player.score), 18, WIDTH / 2, 10)
    draw_lives(screen, WIDTH - 90, 5, player.lives, player_mini_img)
    pygame.display.flip()

pygame.quit()
