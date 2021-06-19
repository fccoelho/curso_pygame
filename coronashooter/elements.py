import pygame
import os


class ElementSprite(pygame.sprite.Sprite):
    """ The basic class of every element in the game.
    Inherits from pygame.sprite.Sprite so pygame can do with it everything it does with sprites
    """

    def __init__(self, image, position, speed=None, new_size=None):
        """ Element constructor
        :param image: the location and name of the desired image for the sprite
        :type image: string
        :param position: the initial position of the element
        :type position: list
        :param speed: the initial speed of the element
        :type speed: list
        :param new_size: the desired size of the loaded image
        :type new_size: list
        """
        pygame.sprite.Sprite.__init__(self)
        # Tries to load the image
        if isinstance(image, str):
            self.image = pygame.image.load(os.path.join('images', image))
        else:
            raise TypeError("image must be of type str")
        # Checks if the image has to be resized and if so, does it
        if new_size:
            self.scale(new_size)
        self.rect = self.image.get_rect()  # gets a pygame.Rect object out of the image
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.speed = speed
        self.set_pos(position)  # sets the position of the sprite
        # sets the speed. If None, the speed is set to (0,2)

    def update(self, dt):
        """ Updates the position of the element
        :param dt: time variation
        :type dt: float (?)
        """
        move_speed = (self.speed * dt / 16,
                      self.speed * dt / 16)  # note that dt=16, so dt/16 == 1
        pos_y = self.rect.center[1] + self.speed*dt
        self.rect.center = (self.rect.center[0], pos_y)
        # self.rect = self.rect.move(move_speed)
        # kills the element if it is out of the screen borders
        if (self.rect.left > self.area.right) or \
                (self.rect.top > self.area.bottom) or \
                (self.rect.right < 0):
            self.kill()
        if (self.rect.bottom < - 40):
            self.kill()

    def get_speed(self):
        return self.speed

    def set_speed(self, speed):
        self.speed = speed

    def get_pos(self):
        # gets the position of the pygame.Rect object
        return (self.rect.center[0],
                self.rect.bottom)

    def set_pos(self, pos):
        # sets the position of the pygame.Rect object
        self.rect.center = (pos[0], pos[1])

    def get_size(self):
        return self.image.get_size()

    def scale(self, new_size):
        # resizes the sprite
        self.image = pygame.transform.scale(self.image, new_size)

    def set_image(self, image, scale):
        self.image = pygame.image.load(os.path.join('images', image))
        self.scale(scale)
