from enum import Enum
import pygame


class CEnemyHunterState:
    def __init__(self, start_pos: pygame.Vector2):
        self.state = HunterState.IDLE
        self.start_pos = pygame.Vector2(start_pos.x, start_pos.y)
        self.chase_sound_channel = None


class HunterState(Enum):
    IDLE = 0
    CHASE = 1
    RETURN = 2
