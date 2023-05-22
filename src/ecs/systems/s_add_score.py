import json
import esper
from src.ecs.components.c_hiscore import CHiScore

from src.ecs.components.c_score import CScore
from src.ecs.components.c_surface import CSurface
from src.engine.service_locator import ServiceLocator


def system_add_score(world: esper.World, score: int):
    score_text_entity = world.get_components(CScore, CSurface)
    # print(score_text_entity)
    c_score = score_text_entity[0][1][0]
    c_score.score += score

    c_surface = score_text_entity[0][1][1]
    world.remove_component(score_text_entity[0][0], CSurface)
    world.add_component(score_text_entity[0][0], CSurface.from_text(f"{c_score.score}", ServiceLocator.fonts_service.get("common"), c_surface.color))

    hi_score_text_entity = world.get_components(CHiScore, CSurface)
    c_hi_score = hi_score_text_entity[0][1][0]
    if c_score.score > c_hi_score.hi_score:
        c_hi_score.hi_score = c_score.score

        c_surface = hi_score_text_entity[0][1][1]
        world.remove_component(hi_score_text_entity[0][0], CSurface)
        world.add_component(hi_score_text_entity[0][0], CSurface.from_text(f"{c_hi_score.hi_score}", ServiceLocator.fonts_service.get("common"), c_surface.color))


