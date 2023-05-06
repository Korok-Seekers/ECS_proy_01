
import esper
import pygame
from src.ecs.components.c_player_weapon import CPlayerWeapon

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.systems.s_show_cooldown import system_show_cooldown

def system_rendering(world:esper.World, screen:pygame.Surface, delta_time:float):
    components = world.get_components(CTransform, CSurface)
    c_pw = world.component_for_entity(1, CPlayerWeapon)
    c_pw.cooldown -= delta_time
    system_show_cooldown(screen, world, c_pw.cooldown)

    c_t:CTransform
    c_s:CSurface
    for _, (c_t, c_s) in components:
        screen.blit(c_s.surf, c_t.pos, area=c_s.area)
        
        
        