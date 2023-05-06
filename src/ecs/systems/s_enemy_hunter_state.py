import esper

from src.ecs.components.c_animation import CAnimation, set_animation
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_enemy_hunter_state import CEnemyHunterState, HunterState
from src.engine.service_locator import ServiceLocator


def system_enemy_hunter_state(world: esper.World, player_entity: int, hunter_info: dict):
    pl_t = world.component_for_entity(player_entity, CTransform)
    components = world.get_components(CEnemyHunterState, CAnimation, CTransform, CVelocity)
    for _, (c_st, c_a, c_t, c_v) in components:
        if c_st.state == HunterState.IDLE:
            _do_enemy_hunter_idle(c_st, c_a, c_t, c_v, pl_t, hunter_info)
        elif c_st.state == HunterState.CHASE:
            _do_enemy_hunter_chase(c_st, c_a, c_t, c_v, pl_t, hunter_info)
        elif c_st.state == HunterState.RETURN:
            _do_enemy_hunter_return(c_st, c_a, c_t, c_v, hunter_info)


def _do_enemy_hunter_idle(c_st: CEnemyHunterState, c_a: CAnimation, c_t: CTransform,
                          c_v: CVelocity, pl_t: CTransform, hunter_info: dict):
    set_animation(c_a, "IDLE")
    c_v.vel.x = 0
    c_v.vel.y = 0

    dist_to_player = c_t.pos.distance_to(pl_t.pos)
    if dist_to_player < hunter_info["distance_start_chase"]:
        ServiceLocator.sounds_service.play(hunter_info["sound_chase"])
        c_st.state = HunterState.CHASE


def _do_enemy_hunter_chase(c_st: CEnemyHunterState, c_a: CAnimation, c_t: CTransform,
                           c_v: CVelocity, pl_t: CTransform, hunter_info: dict):
    set_animation(c_a, "MOVE")
    c_v.vel = (pl_t.pos - c_t.pos).normalize() * hunter_info["velocity_chase"]
    dist_to_origin = c_st.start_pos.distance_to(c_t.pos)
    if dist_to_origin >= hunter_info["distance_start_return"]:
        c_st.state = HunterState.RETURN


def _do_enemy_hunter_return(c_st: CEnemyHunterState, c_a: CAnimation,
                            c_t: CTransform, c_v: CVelocity, hunter_info: dict):
    set_animation(c_a, "MOVE")
    c_v.vel = (c_st.start_pos - c_t.pos).normalize() * hunter_info["velocity_return"]
    dist_to_origin = c_st.start_pos.distance_to(c_t.pos)
    if dist_to_origin <= 2:
        c_t.pos.xy = c_st.start_pos.xy
        c_st.state = HunterState.IDLE
