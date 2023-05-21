import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_enemy import CEnemy

def system_enemy_movement(world: esper.World, timer:float):

    components = world.get_components(CTransform, CVelocity, CEnemy)

    if timer > 4:
        c_t: CTransform
        c_v: CVelocity
        c_e: CEnemy
        for _, (c_t, c_v, c_e) in components:

            if timer > 1:
                c_v.vel.x *= -1

        timer = 0
    return timer

