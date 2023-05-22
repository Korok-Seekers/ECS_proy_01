
import esper
import pygame
from src.create.prefab_creator import create_enemy_spawner, create_start_text

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_surface import CSurface

def system_restart_level(world: esper.World, player_entity: int, level_cfg: dict, screen: pygame.Surface, interface_cfg: dict):
    enemy_spawner = world.get_components(CEnemySpawner)[0][0]

    world.delete_entity(enemy_spawner)

    create_enemy_spawner(world, level_cfg)

    player_surface = world.component_for_entity(player_entity, CSurface)
    player_surface.surf.set_alpha(255)

    create_start_text(world, interface_cfg, screen)







