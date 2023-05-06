import pygame


class SoundsService:
    def __init__(self) -> None:
        self.sounds = {}

    def play(self, path: str) -> None:
        if path not in self.sounds:
            self.sounds[path] = pygame.mixer.Sound(path)
        self.sounds[path].play()

    