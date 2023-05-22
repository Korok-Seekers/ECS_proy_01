
import esper
import pygame
from src.create.prefab_creator import create_input_player, create_interface_text
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_text import CTagText
from src.ecs.systems.s_restart_level import system_restart_level


def system_restart_game(world:esper.World, player_entity:int, level_cfg:dict, interface_info:dict, screen: pygame.Surface):
    system_restart_level(world, player_entity, level_cfg, screen, interface_info)

    text_components = world.get_components(CTagText, CSurface)
    for entity, (c_t, _) in text_components:
        world.delete_entity(entity)

    create_interface_text(world, interface_info, screen)
    create_input_player(world)
