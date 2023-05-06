import pygame
import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet


def system_screen_bullet(world: esper.World, screen: pygame.Surface):
    scr_rect = screen.get_rect()
    components = world.get_components(CTransform, CSurface, CTagBullet)
    for bullet_entity, (c_t, c_s, _) in components:
        bullet_rect = c_s.surf.get_rect(topleft=c_t.pos)
        if not scr_rect.contains(bullet_rect):
            world.delete_entity(bullet_entity)
