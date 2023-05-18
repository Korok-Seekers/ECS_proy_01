import math
import random
import pygame
import esper

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_pause import CTagPause
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_enemy_hunter_state import CEnemyHunterState
from src.engine.service_locator import ServiceLocator


def create_square(world: esper.World, size: pygame.Vector2,
                  pos: pygame.Vector2, vel: pygame.Vector2, col: pygame.Color) -> int:
    cuad_entity = world.create_entity()
    world.add_component(cuad_entity,
                        CSurface(size, col))
    world.add_component(cuad_entity,
                        CTransform(pos))
    world.add_component(cuad_entity,
                        CVelocity(vel))
    return cuad_entity


def create_sprite(world: esper.World, pos: pygame.Vector2, vel: pygame.Vector2,
                  surface: pygame.Surface) -> int:
    sprite_entity = world.create_entity()
    world.add_component(sprite_entity,
                        CTransform(pos))
    world.add_component(sprite_entity,
                        CVelocity(vel))
    world.add_component(sprite_entity,
                        CSurface.from_surface(surface))
    return sprite_entity


def create_enemy_square(world: esper.World, pos: pygame.Vector2, enemy_info: dict):
    enemy_surface = ServiceLocator.images_service.get(enemy_info["image"])
    # vel_max = enemy_info["velocity_max"]
    # vel_min = enemy_info["velocity_min"]
    # vel_range = random.randrange(vel_min, vel_max)
    # velocity = pygame.Vector2(random.choice([-vel_range, vel_range]),
    #                           random.choice([-vel_range, vel_range]))
    enemy_entity = create_sprite(world, pos, pygame.Vector2(0,0), enemy_surface)
    world.add_component(enemy_entity, CTagEnemy())
    # ServiceLocator.sounds_service.play(enemy_info["sound"])


def create_enemy_animated(world: esper.World, pos: pygame.Vector2, enemy_info: dict):
    enemy_surface = ServiceLocator.images_service.get(enemy_info["image"])
    velocity = pygame.Vector2(0, 0)
    enemy_entity = create_sprite(world, pos, velocity, enemy_surface)
    world.add_component(enemy_entity, CEnemyHunterState(pos))
    world.add_component(enemy_entity,
                        CAnimation(enemy_info["animations"]))
    world.add_component(enemy_entity, CTagEnemy())


def create_player_square(world: esper.World, player_info: dict, player_lvl_info: dict) -> int:
    player_sprite = ServiceLocator.images_service.get(player_info["image"])
    size = player_sprite.get_size()
    # size = (size[0] / player_info["animations"]["number_frames"], size[1])
    pos = pygame.Vector2(player_lvl_info["position"]["x"] - (size[0] / 2),
                         player_lvl_info["position"]["y"] - (size[1] / 2))
    vel = pygame.Vector2(0, 0)
    player_entity = create_sprite(world, pos, vel, player_sprite)
    world.add_component(player_entity, CTagPlayer())
    # world.add_component(player_entity,
    #                     CAnimation(player_info["animations"]))
    world.add_component(player_entity, CPlayerState())
    return player_entity


def create_enemy_spawner(world: esper.World, level_data: dict):
    spawner_entity = world.create_entity()
    world.add_component(spawner_entity,
                        CEnemySpawner(level_data["enemy_spawn"]))


def create_input_player(world: esper.World):
    input_left = world.create_entity()
    input_right = world.create_entity()
    input_up = world.create_entity()
    input_down = world.create_entity()

    world.add_component(input_left,
                        CInputCommand("PLAYER_LEFT", pygame.K_LEFT, False))
    world.add_component(input_right,
                        CInputCommand("PLAYER_RIGHT", pygame.K_RIGHT, False))
    world.add_component(input_up,
                        CInputCommand("PLAYER_UP", pygame.K_UP, False))
    world.add_component(input_down,
                        CInputCommand("PLAYER_DOWN", pygame.K_DOWN, False))

    input_fire = world.create_entity()
    world.add_component(input_fire,
                        CInputCommand("PLAYER_FIRE", pygame.K_z, False))

    input_pause = world.create_entity()
    world.add_component(input_pause,
                        CInputCommand("PAUSE", pygame.K_p, True))


def create_bullet(world: esper.World,
                  player_pos: pygame.Vector2,
                  player_size: pygame.Vector2,
                  bullet_info: dict):
    bullet_surface = ServiceLocator.images_service.get(bullet_info["image"])
    bullet_size = bullet_surface.get_rect().size
    pos = pygame.Vector2(player_pos.x + (player_size[0] / 2) - (bullet_size[0] / 2),
                         player_pos.y + (player_size[1] / 2) - (bullet_size[1] / 2))
    vel = pygame.Vector2(0, -bullet_info["velocity"])

    bullet_entity = create_sprite(world, pos, vel, bullet_surface)
    world.add_component(bullet_entity, CTagBullet())
    ServiceLocator.sounds_service.play(bullet_info["sound"])

def create_multiple_bullets(world: esper.World,
                        mouse_pos: pygame.Vector2,
                        player_pos: pygame.Vector2,
                        player_size: pygame.Vector2,
                        bullet_info: dict):
    bullet_surface = ServiceLocator.images_service.get(bullet_info["image"])
    bullet_size = bullet_surface.get_rect().size

    # Calculate the position of the center bullet
    center_pos = pygame.Vector2(player_pos.x + (player_size[0] / 2) - (bullet_size[0] / 2),
                                player_pos.y + (player_size[1] / 2) - (bullet_size[1] / 2))
    vel = (mouse_pos - player_pos)
    vel = vel.normalize() * bullet_info["velocity"]

    # Calculate the positions of the left and right bullets
    left_pos = pygame.Vector2(center_pos.x - (bullet_size[0] / 2), center_pos.y)
    right_pos = pygame.Vector2(center_pos.x + (bullet_size[0] / 2), center_pos.y)

    # Calculate the velocities of the left and right bullets
    left_vel = vel.rotate(30)
    right_vel = vel.rotate(-30)

    # Create the entities for the bullets
    center_bullet = create_sprite(world, center_pos, vel, bullet_surface)
    left_bullet = create_sprite(world, left_pos, left_vel, bullet_surface)
    right_bullet = create_sprite(world, right_pos, right_vel, bullet_surface)

    # Add tags and play sounds
    world.add_component(center_bullet, CTagBullet())
    world.add_component(left_bullet, CTagBullet())
    world.add_component(right_bullet, CTagBullet())
    ServiceLocator.sounds_service.play(bullet_info["sound"])


def create_explosion(world: esper.World, pos: pygame.Vector2, explosion_info: dict):
    explosion_surface = ServiceLocator.images_service.get(explosion_info["image"])
    vel = pygame.Vector2(0, 0)

    explosion_entity = create_sprite(world, pos, vel, explosion_surface)
    world.add_component(explosion_entity, CTagExplosion())
    world.add_component(explosion_entity,
                        CAnimation(explosion_info["animations"]))
    ServiceLocator.sounds_service.play(explosion_info["crash_sound"])
    return explosion_entity

def create_text(world: esper.World, interface_info: dict, screen: pygame.Surface):
    font = pygame.font.Font(interface_info["font"], interface_info["font_size"])
    title_text = interface_info["title"]
    title_color_info = interface_info["title_color"]
    title_color = pygame.Color(title_color_info[0], title_color_info[1], title_color_info[2])
    title_pos = pygame.Vector2(interface_info["title_pos"][0], interface_info["title_pos"][1])
    title_entity = world.create_entity()
    world.add_component(title_entity, CSurface.from_text(title_text, font, title_color))
    world.add_component(title_entity, CTransform(title_pos))

    controls_text = interface_info["controls"]
    controls_color_info = interface_info["controls_color"]
    controls_color = pygame.Color(controls_color_info[0], controls_color_info[1], controls_color_info[2])
    controls_pos = pygame.Vector2(interface_info["controls_pos"][0], interface_info["controls_pos"][1])
    controls_entity = world.create_entity()
    world.add_component(controls_entity, CSurface.from_text(controls_text, font, controls_color))
    world.add_component(controls_entity, CTransform(controls_pos))

    font = pygame.font.Font(interface_info["font"], interface_info["pause_font_size"])
    pause_text = interface_info["pause"]
    pause_pos = pygame.Vector2(screen.get_width() / 2 - font.size(pause_text)[0] / 2, screen.get_height() / 2 - font.size(pause_text)[1] / 2)
    pause_entity = world.create_entity()
    world.add_component(pause_entity, CTransform(pause_pos))
    world.add_component(pause_entity, CTagPause())

