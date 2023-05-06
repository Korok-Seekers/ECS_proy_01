import esper

from src.create.prefab_creator import create_enemy_square, create_enemy_hunter
from src.ecs.components.c_enemy_spawner import CEnemySpawner, SpawnEventData


def system_enemy_spawner(world: esper.World, enemies_data: dict, delta_time: float):
    components = world.get_component(CEnemySpawner)
    c_spw: CEnemySpawner
    for _,  c_spw in components:
        c_spw.current_time += delta_time
        spw_evt: SpawnEventData
        for spw_evt in c_spw.spawn_event_data:
            if c_spw.enemies_to_spawn == 0:
                c_spw.done = True
                return
            if c_spw.current_time >= spw_evt.time and not spw_evt.triggered:
                spw_evt.triggered = True
                if spw_evt.enemy_type == "TypeHunter":
                    create_enemy_hunter(world,
                                        spw_evt.position,
                                        enemies_data[spw_evt.enemy_type])
                    c_spw.enemies_to_spawn -= 1
                else:
                    create_enemy_square(world,
                                        spw_evt.position,
                                        enemies_data[spw_evt.enemy_type])
                    c_spw.enemies_to_spawn -= 1
