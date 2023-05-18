import asyncio
import json
import pygame
import esper
from src.ecs.systems.s_animation import system_animation

from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_collision_enemy_bullet import system_collision_enemy_bullet

from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_pause import system_pause
from src.ecs.systems.s_screen_bounce import system_screen_bounce
from src.ecs.systems.s_screen_player import system_screen_player
from src.ecs.systems.s_screen_bullet import system_screen_bullet

from src.ecs.systems.s_player_state import system_player_state
from src.ecs.systems.s_explosion_kill import system_explosion_kill
from src.ecs.systems.s_enemy_hunter_state import system_enemy_hunter_state

from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_bullet import CTagBullet

from src.ecs.components.c_input_command import CInputCommand, CommandPhase

from src.create.prefab_creator import create_enemy_spawner, create_input_player, create_player_square, create_bullet, create_text


class GameEngine:
    def __init__(self) -> None:
        self._load_config_files()

        pygame.init()
        pygame.display.set_caption(self.window_cfg["title"])
        self.screen = pygame.display.set_mode(
            (self.window_cfg["size"]["w"], self.window_cfg["size"]["h"]),
            pygame.SCALED)

        self.clock = pygame.time.Clock()
        self.is_running = False
        self.is_paused = False
        self.framerate = self.window_cfg["framerate"]
        self.delta_time = 0
        self.bg_color = pygame.Color(self.window_cfg["bg_color"]["r"],
                                     self.window_cfg["bg_color"]["g"],
                                     self.window_cfg["bg_color"]["b"])
        self.ecs_world = esper.World()

        self.num_bullets = 0

    def _load_config_files(self):
        with open("assets/cfg/window.json", encoding="utf-8") as window_file:
            self.window_cfg = json.load(window_file)
        with open("assets/cfg/enemies.json") as enemies_file:
            self.enemies_cfg = json.load(enemies_file)
        with open("assets/cfg/level_01.json") as level_01_file:
            self.level_01_cfg = json.load(level_01_file)
        with open("assets/cfg/player.json") as player_file:
            self.player_cfg = json.load(player_file)
        with open("assets/cfg/player_bullet.json") as player_bullet_file:
            self.player_bullet_cfg = json.load(player_bullet_file)
        with open("assets/cfg/enemy_bullet.json") as enemy_bullet_file:
            self.enemy_bullet_cfg = json.load(enemy_bullet_file)
        with open("assets/cfg/player_explosion.json") as player_explosion_file:
            self.player_explosion_cfg = json.load(player_explosion_file)
        with open("assets/cfg/enemy_explosion.json") as enemy_explosion_file:
            self.enemy_explosion_cfg = json.load(enemy_explosion_file)
        with open("assets/cfg/interface.json", encoding="utf-8") as interface_file:
            self.interface_cfg = json.load(interface_file)

    async def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._process_events()
            self._calculate_time()
            if not self.is_paused:
                self._update()
            await asyncio.sleep(0)
            self._draw()
        self._clean()

    def _create(self):
        create_text(self.ecs_world, self.interface_cfg, self.screen)

        self._player_entity = create_player_square(self.ecs_world, self.player_cfg, self.level_01_cfg["player_spawn"])
        self._player_c_v = self.ecs_world.component_for_entity(self._player_entity, CVelocity)
        self._player_c_t = self.ecs_world.component_for_entity(self._player_entity, CTransform)
        self._player_c_s = self.ecs_world.component_for_entity(self._player_entity, CSurface)

        create_enemy_spawner(self.ecs_world, self.level_01_cfg)
        create_input_player(self.ecs_world)

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            system_input_player(self.ecs_world, event, self._do_action)
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_running = False



    def _update(self):
        system_enemy_spawner(self.ecs_world, self.enemies_cfg, self.delta_time)
        system_movement(self.ecs_world, self.delta_time)

        # system_screen_bounce(self.ecs_world, self.screen)
        system_screen_player(self.ecs_world, self.screen)
        system_screen_bullet(self.ecs_world, self.screen)

        system_collision_enemy_bullet(self.ecs_world, self.enemy_explosion_cfg)
        system_collision_player_enemy(self.ecs_world, self._player_entity,
                                        self.level_01_cfg, self.enemy_explosion_cfg)

        system_explosion_kill(self.ecs_world)

        system_player_state(self.ecs_world)
        # system_enemy_hunter_state(self.ecs_world, self._player_entity, self.enemies_cfg["Hunter"])

        system_animation(self.ecs_world, self.delta_time)

        self.ecs_world._clear_dead_entities()
        self.num_bullets = len(self.ecs_world.get_component(CTagBullet))

    def _draw(self):
        self.screen.fill(self.bg_color)
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()

    def _do_action(self, c_input: CInputCommand):
        # print(c_input.name, c_input.phase)
        if c_input.name == "PLAYER_LEFT":
            if c_input.phase == CommandPhase.START:
                self._player_c_v.vel.x -= self.player_cfg["input_velocity"]
                self.was_paused_left = False
            elif c_input.phase == CommandPhase.END:
                if self.was_paused_left:
                    self.was_paused_left = False
                else:
                    self._player_c_v.vel.x += self.player_cfg["input_velocity"]
        if c_input.name == "PLAYER_RIGHT":
            if c_input.phase == CommandPhase.START:
                self._player_c_v.vel.x += self.player_cfg["input_velocity"]
                self.was_paused_rigth = False
            elif c_input.phase == CommandPhase.END:
                if self.was_paused_rigth:
                    self.was_paused_rigth = False
                else:
                    self._player_c_v.vel.x -= self.player_cfg["input_velocity"]

        if c_input.name == "PLAYER_FIRE" and self.num_bullets < self.level_01_cfg["player_spawn"]["max_bullets"]:
            create_bullet(self.ecs_world, self._player_c_t.pos,
                            self._player_c_s.area.size, self.player_bullet_cfg)

        if c_input.name == "PAUSE":
            self.is_paused = not self.is_paused
            if not self.is_paused:
                self.was_paused_down = True
                self.was_paused_up = True
                self.was_paused_rigth = True
                self.was_paused_left = True
            system_pause(self.ecs_world, self.interface_cfg, self.screen, self._player_entity)

