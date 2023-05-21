import esper
import pygame
from src.create.prefab_creator import create_explosion, create_start_text
from src.ecs.components.c_lives import CLives

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy_bullet import CTagEnemyBullet
from src.ecs.systems.s_game_over import system_game_over
from src.ecs.systems.s_remove_life import system_remove_life
from src.ecs.systems.system_clear_bullets import system_clear_bullets


def system_collision_player_bullet(world: esper.World, player_entity: int,
                                   level_cfg: dict, explosion_info: dict, interface_cfg: dict, screen: pygame.Surface):
    components = world.get_components(CSurface, CTransform, CTagEnemyBullet)
    pl_t = world.component_for_entity(player_entity, CTransform)
    pl_s = world.component_for_entity(player_entity, CSurface)

    pl_rect = pl_s.area.copy()
    pl_rect.topleft = pl_t.pos

    for enemy_entity, (c_s, c_t, _) in components:
        ene_rect = c_s.area.copy()
        ene_rect.topleft = c_t.pos
        if ene_rect.colliderect(pl_rect):
            world.delete_entity(enemy_entity)
            system_clear_bullets(world)
            pl_t.pos.x = level_cfg["player_spawn"]["position"]["x"] - \
                pl_s.area.w / 2
            pl_t.pos.y = level_cfg["player_spawn"]["position"]["y"] - \
                pl_s.area.h / 2
            create_explosion(world, c_t.pos, explosion_info)
            system_remove_life(world)

            c_lives = world.get_components(CLives)[0][1][0]
            if c_lives.lives < 0:
                system_game_over(world, interface_cfg, screen, player_entity)
            else:
                create_start_text(world, interface_cfg, screen)

            break
