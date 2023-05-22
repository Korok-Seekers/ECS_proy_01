import esper
import pygame

from src.ecs.components.c_cooldown import CCooldown
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_text import CTagText
from src.engine.service_locator import ServiceLocator


def system_show_cooldown(world: esper.World, cooldown: float, interface_info: dict):
    components = world.get_components(CCooldown, CSurface, CTagText)

    for entity, (c_cd, c_s, c_tt) in components:
        c_cd.curren_cooldown = round(cooldown)
        total = c_cd.max_cooldown

        world.remove_component(entity, CSurface)

        # create new surface
        font = ServiceLocator.fonts_service.get("common")
        color = pygame.Color(interface_info["cooldown_color"][0], interface_info["cooldown_color"][1], interface_info["cooldown_color"][2])
        g_value = int(color.g * (cooldown / total))
        b_value = int(color.b * (cooldown / total))
        color.g = g_value
        color.b = b_value


        world.add_component(entity, CSurface.from_text(str(c_cd.curren_cooldown), font, color))





