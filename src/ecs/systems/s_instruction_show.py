import pygame
import asyncio

async def system_instruction_show(screen: pygame.Surface):
    # Set up the font
    font = pygame.font.Font(None, 25)

    # Explain the user how to play, arrows for movement and right click for shooting
    text = font.render("Use the arrows to move", True, (255, 255, 255))
    textpos = text.get_rect()
    textpos.centerx = screen.get_rect().centerx
    textpos.centery = screen.get_rect().centery - 150

    # Write some other text
    text2 = font.render("Left click to shoot", True, (255, 255, 255))
    textpos2 = text2.get_rect()
    textpos2.centerx = screen.get_rect().centerx
    textpos2.centery = screen.get_rect().centery - 70

    # Write some other text
    text3 = font.render("Right click to use your special power, you can shoot three bullets", True, (255, 255, 255))
    textpos3 = text2.get_rect()
    textpos3.centerx = screen.get_rect().centerx - 200
    textpos3.centery = screen.get_rect().centery

    # Write some other text
    text4 = font.render("Press enter to start", True, (255, 255, 255))
    textpos4 = text4.get_rect()
    textpos4.centerx = screen.get_rect().centerx
    textpos4.centery = screen.get_rect().centery + 150

    # Write some other text
    text5 = font.render("To pause the game you can press P", True, (255, 255, 255))
    textpos5 = text5.get_rect()
    textpos5.centerx = screen.get_rect().centerx
    textpos5.centery = screen.get_rect().centery + 70

    # Display the text
    screen.blit(text, textpos)
    screen.blit(text2, textpos2)
    screen.blit(text3, textpos3)
    screen.blit(text4, textpos4)
    screen.blit(text5, textpos5)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return True