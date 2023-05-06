import esper

from src.ecs.components.c_animation import CAnimation, set_animation
from src.ecs.components.c_player_state import CPlayerState, PlayerState
from src.ecs.components.c_velocity import CVelocity


def system_player_state(world: esper.World):
    components = world.get_components(CPlayerState, CAnimation, CVelocity)
    for _, (c_st, c_a, c_v) in components:
        if c_st.state == PlayerState.IDLE:
            _do_player_idle(c_st, c_a, c_v)
        elif c_st.state == PlayerState.MOVE:
            _do_player_move(c_st, c_a, c_v)


def _do_player_idle(c_st: CPlayerState, c_a: CAnimation, c_v: CVelocity):
    set_animation(c_a, "IDLE")
    if c_v.vel.magnitude_squared() > 0:
        c_st.state = PlayerState.MOVE


def _do_player_move(c_st: CPlayerState, c_a: CAnimation, c_v: CVelocity):
    set_animation(c_a, "MOVE")
    if c_v.vel.magnitude_squared() <= 0:
        c_st.state = PlayerState.IDLE
