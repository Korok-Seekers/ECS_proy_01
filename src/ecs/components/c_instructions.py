import esper
import pygame

class CInstruccions(esper.Processor):
    def __init__(self, message, duration):
        self.message = message
        self.duration = duration
        self.counter = 0

    def process(self):
        if self.counter < self.duration:
            font = pygame.font.Font(None, 36)
            text = font.render(self.message, 1, (255, 255, 255))
            textpos = text.get_rect(centerx=pygame.display.get_surface().get_width() / 2, centery=pygame.display.get_surface().get_height() / 2)
            pygame.display.get_surface().blit(text, textpos)
            self.counter += 1
        else:
            self.world.remove_processor(self)