import esper

from src.ecs.components.c_lives import CLives
from src.ecs.components.c_surface import CSurface


def system_remove_life(world: esper.World):
    life_text_entity = world.get_component(CLives)
    c_lives = world.component_for_entity(life_text_entity[0], CLives)
    c_lives.lives -= 1

    c_surface = world.component_for_entity(life_text_entity[0], CLives)
    world.remove_component(life_text_entity[0], c_surface)
    world.add_component(life_text_entity[0], CSurface.from_text(f"{c_lives.lives}", c_surface.font, c_surface.color))
    