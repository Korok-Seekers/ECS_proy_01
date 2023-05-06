from typing import Callable
import pygame
import esper
from src.ecs.components.c_input_command import CInputCommand, CommandPhase


def system_input_player(world: esper.World,
                        event: pygame.event.Event,
                        do_action: Callable[[CInputCommand], None]):
    components = world.get_component(CInputCommand)
    for _, c_input in components:
        if event.type == pygame.KEYDOWN and c_input.key == event.key:
            c_input.phase = CommandPhase.START
            do_action(c_input)
        elif event.type == pygame.KEYUP and c_input.key == event.key:
            c_input.phase = CommandPhase.END
            do_action(c_input)
        elif event.type == pygame.MOUSEBUTTONDOWN and c_input.key == event.button:
            c_input.phase = CommandPhase.START
            c_input.mouse_pos = pygame.mouse.get_pos()
            do_action(c_input)
