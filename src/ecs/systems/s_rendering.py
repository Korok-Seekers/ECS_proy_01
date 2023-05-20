
import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface

def system_rendering(world:esper.World, screen:pygame.Surface):
    components = world.get_components(CTransform, CSurface)
    # print(components[0])
    # print(components[0][1][1].heigth)

    # components = sorted(components, key=lambda x: x[1][1].heigth)
    c_t:CTransform
    c_s:CSurface
    # print("components")
    for i in range(3):
        for _, (c_t, c_s) in components:
            if c_s.heigth == i:
                # print(c_s.heigth)
                screen.blit(c_s.surf, c_t.pos, area=c_s.area)
