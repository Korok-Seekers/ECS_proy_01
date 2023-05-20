
import random
import esper
import pygame

from src.ecs.components.c_star import CStar
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity

def system_starfield_loop(world: esper.World, starfield_cfg: dict, screen: pygame.Surface, active_stars: int):
    components = world.get_components(CStar, CTransform)

    for _, (c_star, c_transform) in components:
        if c_transform.pos.y > screen.get_height():
            world.delete_entity(_)

    if active_stars < starfield_cfg["number_of_stars"]:
        # spawn a star
        star = world.create_entity()
        if active_stars >= 23:
            pos = pygame.Vector2(random.randint(0, screen.get_width()), 0)
        else:
            pos = pygame.Vector2(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()))
        color_info = random.choice(starfield_cfg["star_colors"])
        color = pygame.Color(color_info["r"], color_info["g"], color_info["b"])
        blink_rate = random.uniform(starfield_cfg["blink_rate"]["min"], starfield_cfg["blink_rate"]["max"])
        speed_value = random.uniform(starfield_cfg["vertical_speed"]["min"], starfield_cfg["vertical_speed"]["max"])
        speed = pygame.Vector2(0, speed_value)

        world.add_component(star, CTransform(pos))
        world.add_component(star, CStar(blink_rate))
        world.add_component(star, CSurface(pygame.Vector2(1, 1), color, heigth=0))
        world.add_component(star, CVelocity(speed))


