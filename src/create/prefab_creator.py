import math
import random
import pygame
import esper

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_hiscore import CHiScore
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_level import CLevel
from src.ecs.components.c_lives import CLives
from src.ecs.components.c_score import CScore
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_temp_text import CTempText
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_enemy import CEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.c_pause import CPause
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy_bullet import CTagEnemyBullet
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.tags.c_tag_text import CTagText
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
    enemy_entity = create_sprite(world, pos, pygame.Vector2(enemy_info["velocity"], 0), enemy_surface)
    world.add_component(enemy_entity, CEnemy(enemy_info["score"], enemy_info["cooldown_shot"], enemy_info["shot_probability"]))
    # ServiceLocator.sounds_service.play(enemy_info["sound"])


def create_enemy_animated(world: esper.World, pos: pygame.Vector2, enemy_info: dict):
    enemy_surface = ServiceLocator.images_service.get(enemy_info["image"])
    velocity = pygame.Vector2(enemy_info["velocity"], 0)
    enemy_entity = create_sprite(world, pos, velocity, enemy_surface)
    world.add_component(enemy_entity,
                        CAnimation(enemy_info["animations"]))
    world.add_component(enemy_entity, CEnemy(enemy_info["score"], enemy_info["cooldown_shot"], enemy_info["shot_probability"]))


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

    special_power = world.create_entity()
    world.add_component(special_power,
                        CInputCommand("SPECIAL_POWER", pygame.K_x, True))


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

def create_enemy_bullet(world: esper.World,
                        enemy_pos: pygame.Vector2,
                        enemy_size: pygame.Vector2,
                        bullet_info: dict,
                        player_pos: pygame.Vector2):
    bullet_surface = ServiceLocator.images_service.get(bullet_info["image"])
    bullet_size = bullet_surface.get_rect().size
    pos = pygame.Vector2(enemy_pos.x + (enemy_size[0] / 2) - (bullet_size[0] / 2),
                            enemy_pos.y + (enemy_size[1] / 2) - (bullet_size[1] / 2))
    vel = (player_pos - enemy_pos)
    vel = vel.normalize() * bullet_info["velocity"]

    bullet_entity = create_sprite(world, pos, vel, bullet_surface)
    world.add_component(bullet_entity, CTagEnemyBullet())

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

def create_interface_text(world: esper.World, interface_info: dict, screen: pygame.Surface):
    ServiceLocator.sounds_service.play(interface_info["start_sound"])

    font = ServiceLocator.fonts_service.get("common")
    text_color = pygame.Color(interface_info["common_color"][0], interface_info["common_color"][1], interface_info["common_color"][2])

    title_text = interface_info["title"]
    title_color_info = interface_info["title_color"]
    title_color = pygame.Color(title_color_info[0], title_color_info[1], title_color_info[2])
    title_pos = pygame.Vector2(interface_info["title_pos"][0], interface_info["title_pos"][1])
    title_entity = world.create_entity()
    world.add_component(title_entity, CSurface.from_text(title_text, font, title_color, heigth=2))
    world.add_component(title_entity, CTransform(title_pos))
    world.add_component(title_entity, CTagText())

    create_start_text(world, interface_info, screen)


    score_entity = world.create_entity()
    world.add_component(score_entity, CSurface.from_text("0", font, text_color, heigth=2))
    world.add_component(score_entity, CTransform(interface_info["score_pos"]))
    world.add_component(score_entity, CScore())
    world.add_component(score_entity, CTagText())

    high_score_entity = world.create_entity()
    high_score_text = interface_info["high_score"]
    high_score_pos = pygame.Vector2(interface_info["high_score_pos"][0], interface_info["high_score_pos"][1])
    high_score_color_info = interface_info["high_score_color"]
    high_score_color = pygame.Color(high_score_color_info[0], high_score_color_info[1], high_score_color_info[2])
    world.add_component(high_score_entity, CSurface.from_text(high_score_text, font, high_score_color, heigth=2))
    world.add_component(high_score_entity, CTransform(high_score_pos))
    world.add_component(high_score_entity, CHiScore(high_score_text))
    world.add_component(high_score_entity, CTagText())

    lives_entity = world.create_entity()
    lives_pos = pygame.Vector2(interface_info["lives_pos"][0], interface_info["lives_pos"][1])
    lives_entity = world.create_entity()
    world.add_component(lives_entity, CLives())
    c_lives = world.component_for_entity(lives_entity, CLives)
    world.add_component(lives_entity, CTransform(lives_pos))
    world.add_component(lives_entity, CSurface.from_text(str(c_lives.lives), font, text_color, heigth=2))
    world.add_component(lives_entity, CTagText())

    level_entity = world.create_entity()
    level_pos = pygame.Vector2(interface_info["level_pos"][0], interface_info["level_pos"][1])
    level_entity = world.create_entity()
    world.add_component(level_entity, CLevel())
    c_level = world.component_for_entity(level_entity, CLevel)
    world.add_component(level_entity, CSurface.from_text(str(c_level.level), font, text_color, heigth=2))
    world.add_component(level_entity, CTransform(level_pos))
    world.add_component(level_entity, CTagText())

    font = ServiceLocator.fonts_service.get("pause")
    pause_text = interface_info["pause"]
    pause_pos = pygame.Vector2(screen.get_width() / 2 - font.size(pause_text)[0] / 2, screen.get_height() / 2 - font.size(pause_text)[1] / 2)
    pause_entity = world.create_entity()
    pause_color_info = interface_info["pause_color"]
    pause_color = pygame.Color(pause_color_info[0], pause_color_info[1], pause_color_info[2])
    world.add_component(pause_entity, CTransform(pause_pos))
    world.add_component(pause_entity, CPause())
    world.add_component(pause_entity, CSurface.from_text(pause_text, font, pause_color, heigth=2))
    c_surface = world.component_for_entity(pause_entity, CSurface)
    c_surface.surf.set_alpha(0)
    world.add_component(pause_entity, CTagText())


def create_start_text(world: esper.World, interface_info: dict, screen: pygame.Surface):
    start_text = interface_info["start_text"]
    start_color_info = interface_info["start_text_color"]
    start_color = pygame.Color(start_color_info[0], start_color_info[1], start_color_info[2])
    start_font = ServiceLocator.fonts_service.get("start_text")
    start_pos = pygame.Vector2(screen.get_width() / 2- start_font.size(start_text)[0] / 2, screen.get_height() / 2- start_font.size(start_text)[1] / 2)
    start_entity = world.create_entity()
    world.add_component(start_entity, CSurface.from_text(start_text, start_font, start_color, heigth=2))
    world.add_component(start_entity, CTransform(start_pos))
    world.add_component(start_entity, CTempText(interface_info["start_text_time"]))

def create_game_over_text(world: esper.World, interface_info: dict, screen: pygame.Surface):
    game_over_text = interface_info["game_over"]
    game_over_color_info = interface_info["game_over_color"]
    game_over_color = pygame.Color(game_over_color_info[0], game_over_color_info[1], game_over_color_info[2])
    game_over_font = ServiceLocator.fonts_service.get("game_over")
    game_over_pos = pygame.Vector2(screen.get_width() / 2 - game_over_font.size(game_over_text)[0] / 2, screen.get_height() / 2 - game_over_font.size(game_over_text)[1] / 2)
    game_over_entity = world.create_entity()
    world.add_component(game_over_entity, CSurface.from_text(game_over_text, game_over_font, game_over_color, heigth=2))
    world.add_component(game_over_entity, CTransform(game_over_pos))
    world.add_component(game_over_entity, CTempText(interface_info["game_over_time"]))

