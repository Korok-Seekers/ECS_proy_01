import pygame

class CSurface:
    def __init__(self, size:pygame.Vector2, color:pygame.Color, heigth: int=1) -> None:
        self.surf = pygame.Surface(size)
        self.surf.fill(color)
        self.area = self.surf.get_rect()
        self.heigth = heigth

    @classmethod
    def from_surface(cls, surface:pygame.Surface, heigth:int=1):
        c_surf = cls(pygame.Vector2(0,0), pygame.Color(0,0,0), heigth)
        c_surf.surf = surface
        c_surf.area = surface.get_rect()
        return c_surf

    @classmethod
    def from_text(cls, text:str, font:pygame.font.Font, color:pygame.Color, heigth:int=1):
        text_surface = font.render(text, True, color)
        return cls.from_surface(text_surface, heigth)
