import pygame
from pygame.locals import DOUBLEBUF, FULLSCREEN
from fundo import Fundo




class Jogo:
    def __init__(self, size=(800, 800), fullscreen=False):
        actors = {}
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.fundo  = Fundo()
        flags = DOUBLEBUF
        if fullscreen:
            flags |= FULLSCREEN

        self.screen_size = self.screen.get_size()
        pygame.mouse.set_visible( 0 )
        pygame.display.set_caption( 'Corona Shooter' )

    def actors_update(self, dt):
        self.fundo.update(dt)

    def actors_draw(self):
        self.fundo.draw(self.screen)

    def loop(self):
        clock         = pygame.time.Clock()
        dt            = 16
        while True:
            clock.tick( 1000 / dt )

            # Atualiza Elementos
            self.actors_update( dt )

            # Desenhe para o back buffer
            self.actors_draw()
            pygame.display.flip()
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                break


if __name__ == '__main__':
    J = Jogo()
    J.loop()





