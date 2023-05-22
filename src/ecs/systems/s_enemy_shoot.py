import esper
import random
from src.create.prefab_creator import create_enemy_bullet
from src.ecs.components.c_surface import CSurface

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_enemy import CEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer

def system_enemy_shoot(world: esper.World, bullet_info: dict, delta_time: float) -> None:
    player_components = world.get_components(CTransform, CTagPlayer)
    enemy_components = world.get_components(CTransform, CSurface, CEnemy)

    c_t: CTransform
    c_tp: CTagPlayer
    for _, (c_t, c_tp) in player_components:
        c_te: CTransform
        c_ten: CEnemy
        c_s: CSurface
        for _, (c_te, c_s, c_ten) in enemy_components:
            c_ten.timer += delta_time
            if c_ten.timer >= c_ten.cooldown:
                c_ten.timer = 0
                if random.random() < c_ten.probability:
                    create_enemy_bullet(world, c_te.pos, c_s.area.size, bullet_info, c_t.pos)




