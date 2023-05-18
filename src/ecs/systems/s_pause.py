import pygame
import esper
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_pause import CTagPause
from src.engine.service_locator import ServiceLocator


def system_pause(world: esper.World, interface_cfg: dict, player_entity: int, interface_info: dict):
    components = world.get_component(CInputCommand)
    for _, c_input in components:
        if c_input.name == "PAUSE" and c_input.phase == CommandPhase.START:
            # Play the sound
            ServiceLocator.sounds_service.play(interface_info["pause_sound"])
            # get the pause entity with the tag and add the surface component
            component = world.get_component(CTagPause)
            for entity, c_tag in component:
                font = pygame.font.Font(interface_cfg["font"], interface_cfg["pause_font_size"])
                color = pygame.Color(interface_cfg["pause_color"][0], interface_cfg["pause_color"][1], interface_cfg["pause_color"][2])
                c_surface = CSurface.from_text(interface_cfg["pause"], font, color)
                world.add_component(entity, c_surface)

                # pause the game by stopping all velocity and storing them on CTagPause
                moving_entities = world.get_components(CTransform, CVelocity)
                for entity, (c_transform, c_velocity) in moving_entities:
                    c_tag.speeds[entity] = c_velocity.vel
                    c_velocity.vel = pygame.Vector2(0, 0)

                    # save the player speed as 0 to avoid keydown/keyup bugs
                    c_tag.speeds[player_entity] = pygame.Vector2(0, 0)

                # set all input commands except pause to NA to avoid keydown/keyup bugs
                input_entities = world.get_component(CInputCommand)
                for entity, c_input in input_entities:
                    if c_input.name != "PAUSE":
                        c_input.phase = CommandPhase.NA


        elif c_input.name == "PAUSE" and c_input.phase == CommandPhase.END:
            # Play the sound
            ServiceLocator.sounds_service.play(interface_info["unpause_sound"])
            # get the pause entity with the tag and remove the surface component
            component = world.get_component(CTagPause)
            for entity, c_tag in component:
                world.remove_component(entity, CSurface)

                # unpause the game by restoring all velocity from CTagPause
                moving_entities = world.get_components(CTransform, CVelocity)
                for entity, (c_transform, c_velocity) in moving_entities:
                    c_velocity.vel = c_tag.speeds[entity]
                    del c_tag.speeds[entity]







