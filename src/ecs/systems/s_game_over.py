

import esper
import pygame
from src.create.prefab_creator import create_game_over_text
from src.ecs.components.c_input_command import CInputCommand

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_enemy import CEnemy
from src.engine.service_locator import ServiceLocator


def system_game_over(world: esper.World, interface_cfg: dict, screen: pygame.Surface, player_entity: int):
    # delete all anemies
    components = world.get_components(CSurface, CTransform, CEnemy)

    for entity, (c_s, c_t, c_e) in components:
        world.delete_entity(entity)

    player_surface = world.component_for_entity(player_entity, CSurface)
    player_surface.surf.set_alpha(0)

    controls = world.get_components(CInputCommand)
    for e, c in controls:
        world.delete_entity(e)

    # create game over text
    create_game_over_text(world, interface_cfg, screen)

    ServiceLocator.sounds_service.play(interface_cfg["game_over_sound"])

    
