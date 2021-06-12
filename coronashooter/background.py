import pygame
import os
from math import ceil


class Background:
    """ Creates the background of the game
    """

    def __init__(self, image="space.png"):
        """ Background constructor
        :param image: the image to go on the background
        :type image: string
        """

        # loads the image
        image = os.path.join('images', image)
        image = pygame.image.load(image).convert() # .convert() is for performance. Pygame bulls**t

        # sets the initial variables
        self.imagesize = image.get_size()
        self.pos = [0, -1 * self.imagesize[1]]
        screen = pygame.display.get_surface()
        screen_size = screen.get_size()

        # sets the width and height
        w = (ceil(float(screen_size[0]) / self.imagesize[0]) + 1) * \
            self.imagesize[0]
        h = (ceil(float(screen_size[1]) / self.imagesize[1]) + 1) * \
            self.imagesize[1]
        back = pygame.Surface((w, h))

        # blit many copies of the background so it fills the whole back of the screen
        for i in range((back.get_size()[0] // self.imagesize[0])):
            for j in range((back.get_size()[1] // self.imagesize[1])):
                back.blit(image, (i * self.imagesize[0], j * self.imagesize[1]))

        self.image = back


    def update(self, dt):
        """ Moves the background
        :param dt: unused
        :type dt: float (?)
        """
        self.pos[1] += 1
        if self.pos[1] > 0:
            self.pos[1] -= self.imagesize[1]


    def draw(self, screen):
        """ Draw it's image on the given screen
        :param screen: screen to be drawn on
        :type screen: pygame.screen
        """
        screen.blit(self.image, self.pos)


