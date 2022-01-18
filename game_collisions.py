import random
import pygame
import game_sprites


def check_hit_by_enemies(sprite_groups, player):
    hits_by_enemies = pygame.sprite.groupcollide(sprite_groups.players, sprite_groups.enemies, False, False, pygame.sprite.collide_circle)
    for hit in hits_by_enemies:
        now = pygame.time.get_ticks()
        # check if the player in still invulnerable
        if now - player.last_hitted > 1000:
            print("player touched")
            player.lives -= 1
            player.last_hitted = now
            explosion = game_sprites.Explosion(player.rect.center, "sm")
            sprite_groups.all_sprites.add(explosion)
            touched_enemy = hits_by_enemies[hit][0]
            # reduce the lives of ennemies
            is_suicaman = isinstance(touched_enemy, game_sprites.Suicaman)
            is_pampa = isinstance(touched_enemy, game_sprites.Pampa)
            is_boss_lvl1 = isinstance(touched_enemy, game_sprites.Boss_lvl1)
            if is_suicaman or is_pampa or is_boss_lvl1:
                touched_enemy.lives -= 1
                if touched_enemy.lives == 0:
                    expl = game_sprites.Explosion(touched_enemy.rect.center, "lg")
                    sprite_groups.all_sprites.add(expl)
                    touched_enemy.kill()
                else:
                    expl = game_sprites.Explosion(touched_enemy.rect.center, "sm")
                    sprite_groups.all_sprites.add(expl)
            # kill the enemies bullets
            else:
                touched_enemy.kill()
            # reduce the player power
            if player.power > 0:
                player.power -= 1
            # game over
            if player.lives == 0:
                death_explosion = game_sprites.Explosion(player.rect.center, "player")
                sprite_groups.all_sprites.add(death_explosion)


def check_hit_bonus(sprite_groups, player):
    hits_by_bonus = pygame.sprite.spritecollide(player, sprite_groups.bonus, True, pygame.sprite.collide_circle)
    for hb in hits_by_bonus:
        if hb.type == "life" and player.lives < 3:
            player.lives += 1
        if hb.type == "power" and player.power < 2:
            player.power += 1


def check_orbs_hit_dragons(sprite_groups, player):
    orbs_hit_dragons = pygame.sprite.groupcollide(sprite_groups.orbs, sprite_groups.dragons, True, False, pygame.sprite.collide_circle)
    for ohd in orbs_hit_dragons:
        now = pygame.time.get_ticks()
        touched_dragon = orbs_hit_dragons[ohd][0]
        if now - touched_dragon.last_hit > touched_dragon.untouchable_time:
            print("an orb touched a dragon - take 1 life")
            touched_dragon.last_hit = now
            touched_dragon.lives -= 1
            d_expl = game_sprites.Explosion(touched_dragon.rect.center, "sm")
            sprite_groups.all_sprites.add(d_expl)
            if touched_dragon.lives == 0:
                player.score += 100
                dd_expl = game_sprites.Explosion(touched_dragon.rect.center, "lg")
                sprite_groups.all_sprites.add(dd_expl)
                touched_dragon.kill()
                # drop an item at 10% chance
                if random.random() > 0.9:
                    b = game_sprites.Bonus(touched_dragon.rect.center, player)
                    sprite_groups.all_sprites.add(b)
                    sprite_groups.bonus.add(b)
                player.dragon_killed += 1
                if player.dragon_killed < 10:
                    nd = game_sprites.Dragon(sprite_groups)
                    sprite_groups.all_sprites.add(nd)
                    sprite_groups.dragons.add(nd)
                    sprite_groups.enemies.add(nd)


def check_orbs_hit_bees(sprite_groups, player):
    orbs_hit_bees = pygame.sprite.groupcollide(sprite_groups.orbs, sprite_groups.bees, True, False, pygame.sprite.collide_circle)
    for ohb in orbs_hit_bees:
        now = pygame.time.get_ticks()
        touched_bee = orbs_hit_bees[ohb][0]
        if now - touched_bee.last_hit > touched_bee.untouchable_time:
            print("an orb touched a bee - take 1 life")
            touched_bee.last_hit = now
            touched_bee.lives -= 1
            b_expl = game_sprites.Explosion(touched_bee.rect.center, "sm")
            sprite_groups.all_sprites.add(b_expl)
            if touched_bee.lives == 0:
                player.score += 100
                db_expl = game_sprites.Explosion(touched_bee.rect.center, "lg")
                sprite_groups.all_sprites.add(db_expl)
                touched_bee.kill()
                # drop an item at 10% chance
                if random.random() > 0.9:
                    b = game_sprites.Bonus(touched_bee.rect.center, player)
                    sprite_groups.all_sprites.add(b)
                    sprite_groups.bonus.add(b)
                player.bee_killed += 1
                if player.bee_killed < 6:
                    nb = game_sprites.Bee(sprite_groups)
                    sprite_groups.all_sprites.add(nb)
                    sprite_groups.bees.add(nb)
                    sprite_groups.enemies.add(nb)
                else:
                    nd = game_sprites.Dragon(sprite_groups)
                    sprite_groups.all_sprites.add(nd)
                    sprite_groups.dragons.add(nd)
                    sprite_groups.enemies.add(nd)



def check_orbs_hit_suicamans(sprite_groups, player):
    orbs_hit_suicamans = pygame.sprite.groupcollide(sprite_groups.orbs, sprite_groups.suicamans, True, False, pygame.sprite.collide_circle)
    for ohs in orbs_hit_suicamans:
        now = pygame.time.get_ticks()
        touched_suicaman = orbs_hit_suicamans[ohs][0]
        if now - touched_suicaman.last_hit > touched_suicaman.untouchable_time:
            print("an orb touched a suicaman - take 1 life")
            touched_suicaman.last_hit = now
            touched_suicaman.lives -= 1
            s_expl = game_sprites.Explosion(touched_suicaman.rect.center, "sm")
            sprite_groups.all_sprites.add(s_expl)
            if touched_suicaman.lives == 0:
                player.score += 100
                ds_expl = game_sprites.Explosion(touched_suicaman.rect.center, "lg")
                sprite_groups.all_sprites.add(ds_expl)
                touched_suicaman.kill()
                # drop an item at 10% chance
                if random.random() > 0.9:
                    b = game_sprites.Bonus(touched_suicaman.rect.center, player)
                    sprite_groups.all_sprites.add(b)
                    sprite_groups.bonus.add(b)
                player.suicaman_killed += 1
                if player.suicaman_killed < 5 and player.pampa_killed == 0:
                    ns = game_sprites.Suicaman(sprite_groups)
                    sprite_groups.all_sprites.add(ns)
                    sprite_groups.suicamans.add(ns)
                    sprite_groups.enemies.add(ns)
                # after killing 5 suicamans, summon the pampas waves
                if player.suicaman_killed == 5 and not player.pampas_summoned:
                    for i in range(10):
                        np = game_sprites.Pampa()
                        sprite_groups.all_sprites.add(np)
                        sprite_groups.pampas.add(np)
                        sprite_groups.enemies.add(np)
                    player.pampas_summoned = True


def check_orbs_hit_pampas(sprite_groups, player):
    orbs_hit_pampas = pygame.sprite.groupcollide(sprite_groups.orbs, sprite_groups.pampas, True, True, pygame.sprite.collide_circle)
    for ohg in orbs_hit_pampas:
        touched_pampa = orbs_hit_pampas[ohg][0]
        print("an orb touched a pampa")
        player.pampa_killed += 1
        print("pampa killed :%s " % player.pampa_killed)
        player.score += 20
        g_expl = game_sprites.Explosion(touched_pampa.rect.center, "lg")
        sprite_groups.all_sprites.add(g_expl)
        # drop an item at 5% chance
        if random.random() > 0.95:
            b = game_sprites.Bonus(touched_pampa.rect.center, player)
            sprite_groups.all_sprites.add(b)
            sprite_groups.bonus.add(b)
        if player.pampa_killed <= 40:
            np = game_sprites.Pampa()
            sprite_groups.all_sprites.add(np)
            sprite_groups.pampas.add(np)
            sprite_groups.enemies.add(np)


def check_orbs_hit_boss_lvl1(sprite_groups, player):
    orbs_hit_bosses = pygame.sprite.groupcollide(sprite_groups.orbs, sprite_groups.bosses, True, False, pygame.sprite.collide_circle)
    for ohb in orbs_hit_bosses:
        now = pygame.time.get_ticks()
        touched_boss = orbs_hit_bosses[ohb][0]
        if now - touched_boss.last_hit > touched_boss.untouchable_time:
            touched_boss.lives -= 1
            print("an orb touched a boss - boss lives: %s" % touched_boss.lives)
            touched_boss.last_hit = now
            b_expl = game_sprites.Explosion(touched_boss.rect.center, "sm")
            sprite_groups.all_sprites.add(b_expl)
            if touched_boss.lives == 0:
                player.boss_lvl1_defeated = True
                touched_boss.kill()
