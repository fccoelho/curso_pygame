import pygame
from pygame.locals import (DOUBLEBUF,
                           FULLSCREEN,
                           KEYDOWN,
                           KEYUP,
                           K_LEFT,
                           K_RIGHT,
                           QUIT,
                           K_ESCAPE,
                           )
from fundo import Fundo


class Jogo:
    def __init__(self, size=(800, 800), fullscreen=False):
        elementos = {}
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.fundo = Fundo()
        flags = DOUBLEBUF
        if fullscreen:
            flags |= FULLSCREEN

        self.screen_size = self.screen.get_size()
        pygame.mouse.set_visible(0)
        pygame.display.set_caption('Corona Shooter')
        self.run = True

    def atualiza_elementos(self, dt):
        self.fundo.update(dt)

    def desenha_elementos(self):
        self.fundo.draw(self.screen)

    def trata_eventos(self):
        event = pygame.event.poll()
        if event.type == QUIT:
            self.run = False

        if event.type in (KEYDOWN, KEYUP):
            key = event.key
            if key == K_ESCAPE:
                self.run = False

    def loop(self):
        clock = pygame.time.Clock()
        dt = 16
        while self.run:
            clock.tick(1000 / dt)

            self.trata_eventos()

            # Atualiza Elementos
            self.atualiza_elementos(dt)

            # Desenhe no back buffer
            self.desenha_elementos()
            pygame.display.flip()


if __name__ == '__main__':
    J = Jogo()
    J.loop()
