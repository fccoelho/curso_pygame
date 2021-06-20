import pygame
import os


class ElementSprite(pygame.sprite.Sprite):
    """ The basic class of every element in the game.
    Inherits from pygame.sprite.Sprite so pygame can do with it everything it does with sprites
    """

    def __init__(self, image, position, speed=None, new_size=None, direction=(0, 1)):
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
        self.direction = direction  # 1 -> down, -1 -> up
        self.area = screen.get_rect()
        self.speed = speed
        self.set_pos(position)  # sets the position of the sprite
        # sets the speed. If None, the speed is set to (0,2)

    def update(self, dt):
        """ Updates the position of the element
        :param dt: time variation
        :type dt: float (?)
        """
        # move_speed = (self.speed * dt / 16,
        #               self.speed * dt / 16)  # note that dt=16, so dt/16 == 1
        pos_y = self.rect.center[1] + self.direction[1] * self.speed*dt
        self.rect.center = (self.rect.center[0], pos_y)
        # self.rect = self.rect.move(move_speed)
        # kills the element if it is out of the screen borders
        self.check_borders()

    def check_borders(self):
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


class Spaceship(ElementSprite):
    """ class of the controlable element.
    Inherits from ElementSprite (which inherits from pygame.sprite.Sprite) so pygame can do with it whatever it does with sprites.
    """

    def __init__(self, position, lives=0, speed=3.5, image=None, new_size=[83, 248]):
        """ Spaceship constructor
        :param position: the initial position of the element
        :type position: list
        :param lives: how many times the element can get hit before dying
        :type lives: integer (?)
        :param speed: the initial speed of the element on both axis
        :type speed: list
        :param image: the image of the element. The class has a default value that gets overwritten when this parameter is not None
        :type image: string
        :param new_size: the desired size of the sprite. See ElementSprite.scale()
        :type new_size: list
        """
    
        image = "virus.png" if not image else image  # sets the default image
        # calls ElementSprite.__init__()
        super().__init__(image, position, speed, new_size)
        self.set_lives(lives)  # sets the lives of the spaceship

    def get_lives(self):
        return self.lives

    def set_lives(self, lives):
        self.lives = lives


class Enemy(Spaceship):
    def __init__(self, position, lives=0, speed=.35, image=None, size=(75, 50), color='G'):
        """  constructor. Basically the same as Spaceship.__init__(), only difference is the default value for image
        :param position: the initial position of the element
        :type position: list
        :param lives: how many times the element can get hit before dying
        :type lives: integer (?)
        :param speed: the initial speed of the element on both axis
        :type speed: list
        :param image: the image of the element. The class has a default value that gets overwriten when this parameter is not None
        :type image: string
        :param new_size: the desired size of the sprite. See ElementSprite.scale()
        :type new_size: list
        """
        image = f"inimigo1{color}.png" if not image else image
        super().__init__(position, lives, speed, image, size)

    def got_hit(self):
        self.lives -= 1
        if self.lives <= 0:
            self.kill()


class Spider(Enemy):
    def __init__(self, position, lives=0, speed=.35, image=None, size=(75, 50), color='G'):
        """  constructor. Basically the same as Spaceship.__init__(), only difference is the default value for image
        :param position: the initial position of the element
        :type position: list
        :param lives: how many times the element can get hit before dying
        :type lives: integer (?)
        :param speed: the initial speed of the element on both axis
        :type speed: list
        :param image: the image of the element. The class has a default value that gets overwriten when this parameter is not None
        :type image: string
        :param new_size: the desired size of the sprite. See ElementSprite.scale()
        :type new_size: list
        """
        image = f"inimigo1{color}.png" if not image else image
        super().__init__(position, lives, speed, image, size)

    def update(self, dt, playerposx):
        """ Updates the position of the element
        :param dt: time variation
        :type dt: float (?)
        """
        # move_speed = (self.speed * dt / 16,
        #               self.speed * dt / 16)  # note that dt=16, so dt/16 == 1
        pos_y = self.rect.center[1] + self.direction[1] * self.speed*dt
        if playerposx - self.rect.center[0] > 0:
            pos_x = self.rect.center[0] + 1 * self.speed*dt/4
        else:
            pos_x = self.rect.center[0] - 1 * self.speed*dt/4
        self.rect.center = (pos_x, pos_y)
        self.check_borders()


class Shooter(Enemy):
    def __init__(self, position, lives=0, speed=.35, image=None, size=(60, 45), color='G'):
        """  constructor. Basically the same as Spaceship.__init__(), only difference is the default value for image
        :param position: the initial position of the element
        :type position: list
        :param lives: how many times the element can get hit before dying
        :type lives: integer (?)
        :param speed: the initial speed of the element on both axis
        :type speed: list
        :param image: the image of the element. The class has a default value that gets overwriten when this parameter is not None
        :type image: string
        :param new_size: the desired size of the sprite. See ElementSprite.scale()
        :type new_size: list
        """
        image = f"inimigo2{color}.png" if not image else image
        super().__init__(position, lives, speed, image, size)
        self.direction = (1, 0)

    def update(self, dt, playerposx):
        """ Updates the position of the element
        :param dt: time variation
        :type dt: float (?)
        """
        # move_speed = (self.speed * dt / 16,
        #               self.speed * dt / 16)  # note that dt=16, so dt/16 == 1
        pos_x = self.rect.center[0]
        pos_y = self.rect.center[1]
        if pos_y < 50:
            pos_y += self.speed*dt
        # mas esse aí é o papel do teste
        # ERA ESSE OR POBLEMAAAAAAAAAAAAAA (TT.TT  )
        if pos_x >= 580:
            self.direction = (-0.71, 0)
        elif pos_x <= 40:
            self.direction = (1, 0)
        pos_x += self.direction[0]*self.speed*dt/4
        self.rect.center = (pos_x, pos_y)
        self.check_borders()
