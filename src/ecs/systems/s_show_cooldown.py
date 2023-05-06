import esper
import pygame

from src.ecs.components.c_player_weapon import CPlayerWeapon

def system_show_cooldown(screen: pygame.Surface, world: esper.World, cooldown: float):

    c_pw = world.component_for_entity(1, CPlayerWeapon)

    """Show cooldown of player weapon"""
    if cooldown > 0.0:
        # Show cooldown
        font = pygame.font.SysFont("Arial", 12)
        text = font.render(f"Cooldown for triple shot: {cooldown:.2f} - Current Weapon: {c_pw.weapon}", True, (255, 255, 255))
        screen.blit(text, (0, 0))

    else:
        # Show the same info but cooldown on 0s
        font = pygame.font.SysFont("Arial", 12)
        text = font.render(f"Cooldown for triple shot: {0.0:.2f} - Current Weapon: {c_pw.weapon}", True, (255, 255, 255))
        screen.blit(text, (0, 0))

    