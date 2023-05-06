

import esper
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_enemy_hunter_state import CEnemyHunterState
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.create.prefab_creator import create_explosion


def system_collision_enemy_bullet(world: esper.World, explosion_info: dict):
    components_enemy = world.get_components(CSurface, CTransform, CTagEnemy)
    components_bullet = world.get_components(CSurface, CTransform, CTagBullet)
    _, component_spawner = world.get_component(CEnemySpawner)[0]
    for enemy_entity, (c_s, c_t, c_ene) in components_enemy:
        ene_rect = c_s.area.copy()
        ene_rect.topleft = c_t.pos
        for bullet_entity, (c_b_s, c_b_t, _) in components_bullet:
            bull_rect = c_b_s.area.copy()
            bull_rect.topleft = c_b_t.pos
            if ene_rect.colliderect(bull_rect):
                component_spawner.enemies_to_kill -= 1
                world.delete_entity(enemy_entity)
                world.delete_entity(bullet_entity)
                create_explosion(world, c_t.pos, explosion_info)
