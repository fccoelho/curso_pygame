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
from background import Background
from elements import ElementSprite
import random


class Game:
    def __init__(self, size=(800, 800), fullscreen=False):
        self.elements = {}
        pygame.init()
        flags = DOUBLEBUF
        # info = pygame.display.Info()
        # screen_width, screen_height = info.current_w, info.current_h
        # window_width, window_height = screen_width-10, screen_height-50
        if fullscreen:
            flags |= FULLSCREEN
        self.screen = pygame.display.set_mode(
            size, flags)
        self.background = Background()

        self.screen_size = self.screen.get_size()
        pygame.mouse.set_visible(0)
        pygame.display.set_caption('Corona Shooter')
        self.run = True

    def update_elements(self, dt):
        self.background.update(dt)

    def draw_elements(self):
        self.background.draw(self.screen)
        self.spaceship.draw(self.screen)
        for el in self.elements['coronavirus']:
            el.draw(self.screen)

    def handle_events(self):
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
        self.elements['coronavirus'] = [pygame.sprite.RenderPlain(Virus([120, 50]))]
        self.spaceship = pygame.sprite.RenderPlain(Spaceship([200, 400], 5))
        while self.run:
            clock.tick(1000 / dt)

            self.handle_events()

            # Atualiza Elementos
            self.update_elements(dt)

            # Desenhe no back buffer
            self.draw_elements()
            pygame.display.flip()


class Spaceship(ElementSprite):
    def __init__(self, position, lives=0, speed=[0, 0], image=None, new_size=[83, 248]):
        self.acceleration = [3, 3]
        if not image:
            image = "syringe.png"
        super().__init__(image, position, speed, new_size)
        self.set_lives(lives)

    def get_lives(self):
        return self.lives

    def set_lives(self, lives):
        self.lives = lives


class Virus(Spaceship):
    def __init__(self, position, lives=0, speed=None, image=None, size=(100, 100)):
        if not image:
            image = "virus.png"
        super().__init__(position, lives, speed, image, size)


if __name__ == '__main__':
    G = Game()
    G.loop()
