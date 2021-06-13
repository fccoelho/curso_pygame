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
        """ Create the object that will control the game
        
        :param size: desired size of the screen
        :type size: tuple
        :param fullscreen: wether the game will be played on fullscreen or not
        :type fullscreen: boolean
        """
        self.elements = {}  # create the dict which will have all elements of the game
        pygame.init() # Initiate the pygame module
        flags = DOUBLEBUF | FULLSCREEN if fullscreen else DOUBLEBUF # set the display flags
        self.screen = pygame.display.set_mode(size, flags) # create the display with the set size and flags
        self.background = Background() # create the background object
        pygame.display.set_caption('Corona Shooter') # set the game's window title
        pygame.mouse.set_visible(0) # make the mouse cursor invisible
        self.run = True 
        self.loop() # start running the game

    def update_elements(self, dt):
        """ Updates the background so it feels like moving

        :param dt: unused
        :type dt: float (?)
        """
        self.background.update(dt)

    def draw_elements(self):
        """ Draw the elements onto the screen.
        This is done by passing the screen as a parameter to the element that will draw itself on the screen.
        """
        self.background.draw(self.screen) # draw the background
        self.spaceship.draw(self.screen) # draw the spaceship
        for el in self.elements['coronavirus']:
            el.draw(self.screen) # draw all other elements

    def handle_events(self):
        """ Handle each event in the event queue.
        This is basically only used for the user to control the spaceship and to quit the game
        """
        event = pygame.event.poll()
        if event.type == pygame.QUIT: # handle window quit (the "x" on top right corner)
            self.run = False

        # handle keyboard input
        if event.type in (KEYDOWN, KEYUP):
            key = event.key
            if key == K_ESCAPE: # handle keyboard quit
                self.run = False 

    def loop(self):
        """ Main game loop
        """
        clock = pygame.time.Clock() # create the clock object
        dt = 16 # defines the effective speed of the game
        self.elements['coronavirus'] = [pygame.sprite.RenderPlain(Virus([120, 50]))] # prepare the coronavirus sprite
        self.spaceship = pygame.sprite.RenderPlain(Spaceship([200, 400], 5)) # prepare the spacechip sprite
        while self.run:
            clock.tick(1000 / dt)

            # Handle the user interaction
            self.handle_events() 

            # Handle the position and colision updates
            self.update_elements(dt)

            # Draw the elements on their new positions. Right now only works for the background
            # The elements are drawn on the backbuffer, which is later on flipped to become the frontbuffer
            self.draw_elements()
            pygame.display.flip()
        pygame.quit() # kill the program


class Spaceship(ElementSprite):
    """ class of the controlable element.
    Inherits from ElementSprite (which inherits from pygame.sprite.Sprite) so pygame can do with it whatever it does with sprites.
    """
    def __init__(self, position, lives=0, speed=[0, 0], image=None, new_size=[83, 248]):
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
        self.acceleration = [3, 3] # sets the initial acceleration of the spaceship
        image = "syringe.png" if not image else image # sets the default image
        super().__init__(image, position, speed, new_size) # calls ElementSprite.__init__()
        self.set_lives(lives) # sets the lives of the spaceship

    def get_lives(self):
        return self.lives

    def set_lives(self, lives):
        self.lives = lives


class Virus(Spaceship):
    def __init__(self, position, lives=0, speed=None, image=None, size=(100, 100)):
        """ Virus constructor. Basically the same as Spaceship.__init__(), only difference is the default value for image
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
        image = "virus.png" if not image else image
        super().__init__(position, lives, speed, image, size)


if __name__ == '__main__':
    G = Game()
    