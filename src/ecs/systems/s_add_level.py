
import esper
from src.ecs.components.c_level import CLevel
from src.ecs.components.c_surface import CSurface
from src.engine.service_locator import ServiceLocator


def system_add_level(world: esper.World):
    level_text_entity = world.get_components(CLevel, CSurface)
    c_level = level_text_entity[0][1][0]
    c_level.level += 1

    c_surface = level_text_entity[0][1][1]
    world.remove_component(level_text_entity[0][0], CSurface)
    world.add_component(level_text_entity[0][0], CSurface.from_text(f"{c_level.level}", ServiceLocator.fonts_service.get("common"), c_surface.color))

