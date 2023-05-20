import json
import pygame


class FontsService:
    def __init__(self) -> None:
        self._fonts = {}

    def get(self, name: str) -> pygame.Surface:
        with open("assets/cfg/interface.json", encoding="utf-8") as interface_file:
            interface_cfg = json.load(interface_file)
        if name not in self._fonts:
            font = pygame.font.Font(interface_cfg["font"], interface_cfg[name+"_size"])
            self._fonts[name] = font
        return self._fonts[name]
