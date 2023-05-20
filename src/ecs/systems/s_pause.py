import pygame
import esper
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_pause import CPause
from src.engine.service_locator import ServiceLocator


def system_pause(world: esper.World, interface_cfg: dict, player_entity: int):
    components = world.get_component(CInputCommand)
    for _, c_input in components:
        if c_input.name == "PAUSE" and c_input.phase == CommandPhase.START:
            # Play the sound
            ServiceLocator.sounds_service.play(interface_cfg["pause_sound"])
            # get the pause entity with the tag and add the surface component
            component = world.get_component(CPause)
            for entity, c_tag in component:
                c_surface = world.component_for_entity(entity, CSurface)
                # change the alpha value of the surface to 128
                c_surface.surf.set_alpha(255)

                # pause the game by stopping all velocity and storing them on CPause
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
            ServiceLocator.sounds_service.play(interface_cfg["unpause_sound"])
            # get the pause entity with the tag and remove the surface component
            component = world.get_component(CPause)
            for entity, c_tag in component:
                c_surface = world.component_for_entity(entity, CSurface)
                # change the alpha value of the surface to 0
                c_surface.surf.set_alpha(0)

                # unpause the game by restoring all velocity from CPause
                moving_entities = world.get_components(CTransform, CVelocity)
                for entity, (c_transform, c_velocity) in moving_entities:
                    c_velocity.vel = c_tag.speeds[entity]
                    del c_tag.speeds[entity]


