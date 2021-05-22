import pygame
from pygame.locals import (DOUBLEBUF,
                           FULLSCREEN,
                           KEYDOWN,
                           KEYUP,
                           K_LEFT,
                           K_RIGHT,
                           QUIT,
                           K_ESCAPE
                           )
from fundo import Fundo
from elementos import ElementoSprite
import random


class Jogo:
    def __init__(self, size=(800, 800), fullscreen=False):
        self.elementos = {}
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
        self.nave.draw(self.screen)
        for el in self.elementos['virii']:
            el.draw(self.screen)

    def trata_eventos(self):
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            self.run = False

        if event.type in (KEYDOWN, KEYUP):
            key = event.key
            if key == K_ESCAPE:
                self.run = False

    def loop(self):
        clock = pygame.time.Clock()
        dt = 16
        self.elementos['virii'] = [pygame.sprite.RenderPlain(Virus([120, 50]))]
        self.nave = pygame.sprite.RenderPlain(Nave([200, 400], 5))
        while self.run:
            clock.tick(1000 / dt)

            self.trata_eventos()

            # Atualiza Elementos
            self.atualiza_elementos(dt)

            # Desenhe no back buffer
            self.desenha_elementos()
            pygame.display.flip()


class Nave(ElementoSprite):
    def __init__(self, position, lives=0, speed=[0, 0], image=None, new_size=[83, 248]):
        self.acceleration = [3, 3]
        if not image:
            image = "seringa.png"
        super().__init__(image, position, speed, new_size)
        self.set_lives(lives)

    def get_lives(self):
        return self.lives

    def set_lives(self, lives):
        self.lives = lives


class Virus(Nave):
    def __init__(self, position, lives=0, speed=None, image=None, size=(100, 100)):
        if not image:
            image = "virus.png"
        super().__init__(position, lives, speed, image, size)


if __name__ == '__main__':
    J = Jogo()
    J.loop()
