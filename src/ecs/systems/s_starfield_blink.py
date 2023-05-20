import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_star import CStar


def system_starfield_blink(world: esper.World, deltatime: float):
    components = world.get_components(CStar, CSurface)

    for _, (c_tag, c_surface) in components:
        c_tag.blink_timer += deltatime
        if c_tag.blink_timer >= c_tag.blink_rate:
            c_tag.blink_timer = 0.0
            c_tag.blink_on = not c_tag.blink_on
            if c_tag.blink_on:
                c_surface.surf.set_alpha(255)
            else:
                c_surface.surf.set_alpha(0)

