

import esper
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_level import CLevel
from src.ecs.components.c_lives import CLives
from src.ecs.components.c_score import CScore
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_enemy import CEnemy
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.create.prefab_creator import create_explosion
from src.ecs.systems.s_add_score import system_add_score
from src.ecs.systems.s_restart_level import system_restart_level
from src.ecs.systems.s_add_level import system_add_level


def system_collision_enemy_bullet(world: esper.World, explosion_info: dict, level_cfg: dict, player_entity: int):
    components_enemy = world.get_components(CSurface, CTransform, CEnemy)
    components_bullet = world.get_components(CSurface, CTransform, CTagBullet)
    _, component_spawner = world.get_component(CEnemySpawner)[0]
    for enemy_entity, (c_s, c_t, c_ene) in components_enemy:
        ene_rect = c_s.area.copy()
        ene_rect.topleft = c_t.pos
        for bullet_entity, (c_b_s, c_b_t, _) in components_bullet:
            bull_rect = c_b_s.area.copy()
            bull_rect.topleft = c_b_t.pos
            if ene_rect.colliderect(bull_rect):
                score = c_ene.score
                system_add_score(world, score)

                component_spawner.enemies_to_kill -= 1
                world.delete_entity(enemy_entity)
                world.delete_entity(bullet_entity)
                create_explosion(world, c_t.pos, explosion_info)

                n_enemies = len(world.get_components(CEnemy))

                if n_enemies <= 1:
                    system_restart_level(world, player_entity, level_cfg)
                    system_add_level(world)



