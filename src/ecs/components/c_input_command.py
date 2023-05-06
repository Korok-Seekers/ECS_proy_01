from enum import Enum
import pygame


class CInputCommand:
    def __init__(self, name: str, key: int) -> None:
        self.name = name
        self.key = key
        self.phase = CommandPhase.NA
        self.mouse_pos = pygame.Vector2(0, 0)


class CommandPhase(Enum):
    NA = 0
    START = 1
    END = 2
