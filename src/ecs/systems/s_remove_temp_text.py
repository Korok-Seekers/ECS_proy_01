import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_temp_text import CTempText
from src.ecs.components.c_transform import CTransform


def system_remove_temp_text(world: esper.World, delta_time: float):
    components = world.get_components(CTempText, CSurface, CTransform)

    c_t: CTempText
    for entity, (c_t, _, _) in components:
        c_t.timer -= delta_time
        if c_t.timer <= 0:
            world.delete_entity(entity)


