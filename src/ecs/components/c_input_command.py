from enum import Enum
import pygame


class CInputCommand:
    def __init__(self, name: str, key: int, toggle: bool) -> None:
        self.name = name
        self.key = key
        self.phase = CommandPhase.NA
        self.mouse_pos = pygame.Vector2(0, 0)
        self.toggle = toggle


class CommandPhase(Enum):
    NA = 0
    START = 1
    END = 2
