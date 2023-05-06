import pygame


class ImagesService:
    def __init__(self) -> None:
        self._images = {}

    def get(self, path: str) -> pygame.Surface:
        if path not in self._images:
            self._images[path] = pygame.image.load(path).convert_alpha()
        return self._images[path]