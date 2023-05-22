
import esper
from src.ecs.components.tags.c_tag_enemy_bullet import CTagEnemyBullet
from src.engine.service_locator import ServiceLocator

def system_clear_bullets(world: esper.World):
    for bullet_entity, (c_teb) in world.get_components(CTagEnemyBullet):
        world.delete_entity(bullet_entity)
