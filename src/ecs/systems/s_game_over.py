

import json
import esper
import pygame
from src.create.prefab_creator import create_game_over_text, create_restart_text
from src.ecs.components.c_hiscore import CHiScore
from src.ecs.components.c_input_command import CInputCommand

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_enemy import CEnemy
from src.ecs.components.c_velocity import CVelocity
from src.engine.service_locator import ServiceLocator


def system_game_over(world: esper.World, interface_cfg: dict, screen: pygame.Surface, player_entity: int):
    # delete all anemies
    components = world.get_components(CSurface, CTransform, CEnemy)

    for entity, (c_s, c_t, c_e) in components:
        world.delete_entity(entity)

    player_surface = world.component_for_entity(player_entity, CSurface)
    player_surface.surf.set_alpha(0)
    player_speed = world.component_for_entity(player_entity, CVelocity)
    player_speed.vel = pygame.Vector2(0, 0)

    controls = world.get_components(CInputCommand)
    for e, c in controls:
        world.delete_entity(e)

    # create game over text
    create_game_over_text(world, interface_cfg, screen)
    restart_id = create_restart_text(world, interface_cfg, screen)

    ServiceLocator.sounds_service.play(interface_cfg["game_over_sound"])

    hi_score_text_entity = world.get_components(CHiScore, CSurface)
    c_hi_score = hi_score_text_entity[0][1][0]

    #  save new high score to file
    with open("assets/cfg/interface.json", "r") as file:
        jsonfile = json.load(file)
        jsonfile["high_score"] = c_hi_score.hi_score
        # print(jsonfile)
        file.close()
    with open("assets/cfg/interface.json", "w") as filew:
        filew.write(json.dumps(jsonfile, indent=4))
        filew.close()


    return restart_id


