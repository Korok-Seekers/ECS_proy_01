import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_player_weapon import CPlayerWeapon
from src.ecs.components.c_surface import CSurface   
from src.engine.service_locator import ServiceLocator

def system_weapon_change(world: esper.World, player_entity: int):
    c_pl_wp = world.component_for_entity(player_entity, CPlayerWeapon)
    if c_pl_wp.cooldown <= 0.0:
        world.remove_component(player_entity, CSurface)
        c_pl_wp.set_weapon()
        sprite_surface = ServiceLocator.images_service.get(c_pl_wp.sprite)
        c_animation = world.component_for_entity(player_entity, CAnimation)
        c_animation.curr_frame = c_animation.animations_list[c_animation.curr_anim].start
        c_animation.curr_anim = 0
        world.add_component(player_entity, CSurface.from_surface(sprite_surface))
        return
    if c_pl_wp.weapon == "multiple":
        world.remove_component(player_entity, CSurface)
        c_pl_wp.set_weapon()
        sprite_surface = ServiceLocator.images_service.get(c_pl_wp.sprite)
        c_animation = world.component_for_entity(player_entity, CAnimation)
        c_animation.curr_frame = c_animation.animations_list[c_animation.curr_anim].start
        c_animation.curr_anim = 0
        world.add_component(player_entity, CSurface.from_surface(sprite_surface))
        c_pl_wp.number_of_bullets = 0
        c_pl_wp.reset_cooldown()
        
    
    