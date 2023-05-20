import esper

from src.ecs.components.c_lives import CLives
from src.ecs.components.c_surface import CSurface
from src.engine.service_locator import ServiceLocator


def system_remove_life(world: esper.World):
    life_text_entity = world.get_component(CLives)[0][0]
    c_lives = world.component_for_entity(life_text_entity, CLives)
    c_lives.lives -= 1

    c_surface = world.component_for_entity(life_text_entity, CSurface)
    world.remove_component(life_text_entity, CSurface)
    world.add_component(life_text_entity, CSurface.from_text(f"{c_lives.lives}", ServiceLocator.fonts_service.get("common"), c_surface.color))
