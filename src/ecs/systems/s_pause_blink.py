import esper

from src.ecs.components.c_pause import CPause
from src.ecs.components.c_surface import CSurface


def system_pause_blink(world: esper.World, deltatime: float, is_paused: bool):
    components = world.get_component(CPause)
    for _, c_pause in components:
        c_surface = world.component_for_entity(_, CSurface)
        if is_paused:
            if c_pause.blink_on:
                c_surface.surf.set_alpha(255)
            else:
                c_surface.surf.set_alpha(0)

            c_pause.blink_timer += deltatime
            if c_pause.blink_timer >= c_pause.blink_rate:
                c_pause.blink_timer = 0.0
                c_pause.blink_on = not c_pause.blink_on
        else:
            c_pause.blink_on = False
            c_pause.blink_timer = 0.0




