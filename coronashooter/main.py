import pygame
from pygame.locals import (DOUBLEBUF,
                           FULLSCREEN,
                           KEYDOWN,
                           KEYUP,
                           K_LEFT,
                           K_RIGHT,
                           QUIT,
                           K_ESCAPE, K_UP, K_DOWN, K_RCTRL, K_LCTRL
                           )
from background import Background
from elements import *
import random



class Game:
    def __init__(self, size=(640, 640), fullscreen=False):
        """ Creates the object that will control the game

        :param size: desired size of the screen
        :type size: tuple
        :param fullscreen: whether the game will be played on fullscreen or not
        :type fullscreen: boolean
        """
        self.elements = {}  # creates the dict which will have all elements of the game
        self.enemies = []
        self.shoots = []
        self.spwcounter = 45
        self.colcounter = 0
        self.color = 'G'
        pygame.init()  # Initiates the pygame module
        flags = DOUBLEBUF | FULLSCREEN if fullscreen else DOUBLEBUF  # sets the display flags
        # creates the display with the set size and flags
        self.screen = pygame.display.set_mode(size, flags)
        # creates the background object
        self.background = Background('fundoG.png')
        # sets the game's window title
        pygame.display.set_caption('PC Virus Shooter')
        pygame.mouse.set_visible(0)  # makes mouse cursor invisible
        self.run = True
        self.level = 1
        self.loop()  # starts running the game

    def update_elements(self, dt):
        """ Updates the background so it feels like moving

        :param dt: unused
        :type dt: float (?)
        """
        self.background.update(dt)
        for enemy in self.enemies:
            enemy[0].update(dt, self.player.rect.center[0])
        for shoot in self.shoots:
            shoot[0].update(dt)

    def draw_elements(self):
        """ Draws the elements onto the screen.
        This is done by passing the screen as a parameter to the element that will draw itself on the screen.
        """
        self.background.draw(self.screen)  # draw the background
        for element in self.elements.values():
            element.draw(self.screen)
        for enemy in self.enemies:
            enemy[1].draw(self.screen)
        for shoot in self.shoots:
            shoot[1].draw(self.screen)

    def handle_events(self, event, dt=1000):
        """ Handles each event in the event queue.
        This is basically only used for the user to control the spaceship and quit the game
        """
        # handles window quit (the "x" on top right corner)
        if event.type == pygame.QUIT or self.player.isdead:
            self.run = False
        # handles keyboard input
        if event.type in (KEYDOWN,):
            key = event.key
            if key == K_ESCAPE:  # handles keyboard quit
                self.run = False

    def spawn(self):
        pos_x = random.randint(0, 640)
        enemy_type = random.randint(0,1)
        if self.spwcounter > 60:
            if enemy_type == 0:
                enemy = Shooter([pos_x, -25], color=self.color)
            elif enemy_type == 1:
                enemy = Spider([pos_x, -25], color=self.color)
            self.enemies.append([enemy, pygame.sprite.RenderPlain(enemy)])
            self.spwcounter = 0
        else:
            self.spwcounter += 1

    def handle_collision(self):
        for enemy in self.enemies:
            plyr_collision = self.player.rect.colliderect(enemy[0].rect)
            if plyr_collision and self.colcounter <= 0:
                print('ui')
                self.player.got_hit()
                self.colcounter = 60
            for shoot in self.shoots:
                enemy_collision = enemy[0].rect.colliderect(shoot[0].rect)
                if enemy_collision:
                    enemy[0].got_hit()
                    self.player.add_score()
                    if enemy[0].get_lives() <= 0:
                        self.enemies.remove(enemy)
                    self.shoots.remove(shoot)
        if self.colcounter > 0:
            self.colcounter -= 1

    def loop(self):
        """ Main game loop
        """
        clock = pygame.time.Clock()  # creates the clock object
        dt = 16  # defines the effective speed of the game
        self.player = Player([320, 540], 5)
        self.elements['player'] = pygame.sprite.RenderPlain(
            self.player)  # prepares the spaceship sprite
        while self.run:
            clock.tick(1000 / dt)
            event = pygame.event.poll()
            # Handles the user interaction
            self.player.update(dt)
            self.player.shoot(event, self.shoots)
            self.handle_events(event, dt)
            self.handle_collision()
            self.spawn()
            # Handles the position and colision updates
            self.update_elements(dt)

            # Draw the elements on their new positions. Right now only works for the background
            # The elements are drawn on the backbuffer, which is later on flipped to become the frontbuffer
            self.draw_elements()
            pygame.display.flip()
        pygame.quit()  # kill the program



class Player(Spaceship):
    def __init__(self, position, lives=3, speed=.5, image=None, new_size=(27, 36)):
        if not image:
            image = "nave1.png"
        super().__init__(position, lives, speed, image, new_size)
        self.direction = (0, 0)
        self.vel = (0,0)
        self.max_vel = .5
        self.acc = (0,0)
        self.score = 0
        self.size = new_size
        self.isdead = False

    def update(self, dt):
        new_acc = [0,0]
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            new_acc[0] -= 1
        if keys[K_RIGHT]:
            new_acc[0] += 1
        if keys[K_UP]:
            new_acc[1] -= 1
        if keys[K_DOWN]:
            new_acc[1] += 1
        
        new_acc = tuple(new_acc)
        if new_acc != self.acc:
            self.acc = new_acc
            if self.acc[0] == 0:
                self.set_image('nave1.png', self.size)
            elif self.acc[0] == 1:
                self.set_image('nave2.png', self.size)
            elif self.acc[0] == -1:
                self.set_image('nave3.png', self.size)

        self.vel = (self.vel[0]+self.acc[0]*dt/100, self.vel[1]+self.acc[1]*dt/100)
        self.normalize_vel()
        
        pos_x = self.rect.center[0] + self.vel[0]*dt
        pos_y = self.rect.center[1] + self.vel[1]*dt

        # Reduce the velocity, as of friction
        self.vel = (self.vel[0]*9/10, self.vel[1]*9/10)
        if abs(self.vel[0])<0.01:
            self.vel = (0, self.vel[1])
        if abs(self.vel[1])<0.01:
            self.vel = (self.vel[0], 0)

        if pos_x < 0:
            pos_x = 640
        elif pos_x > 640:
            pos_x = 0
        if pos_y < 0:
            pos_y = 0
        elif pos_y > 640:
            pos_y = 640
        self.rect.center = (pos_x, pos_y)

    def shoot(self, event, shoots):
        if event.type in (KEYDOWN,):
            key = event.key
            if key == K_LCTRL:
                laser = Laser((self.rect.center[0], self.rect.top))
                shoots.append([laser, pygame.sprite.RenderPlain(laser)])

    def normalize_vel(self):
        abs_vel = (self.vel[0]**2+self.vel[1]**2)**.5
        if abs_vel>self.max_vel:
            self.vel = (self.vel[0]/abs_vel*self.max_vel, self.vel[1]/abs_vel*self.max_vel)


    def got_hit(self):
        self.lives -= 1
        if self.lives <= 0:
            self.isdead = True

    def get_pos(self):  # perdao
        return (self.rect.center[0], self.rect.center[1])

    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score
        print(self.score)

    def add_score(self):
        self.score += 1


class Laser(ElementSprite):
    def __init__(self, position, speed=.6, image=None):
        if not image:
            image = "tironave1.png"
        super().__init__(image, position, speed, direction=(0, -1))


# como faz pra jogar mesmo/ foi de agora a pergunta?
# foi, nao sei como faz.. #so ta rodando pro edu :(
# :.3 oiඞNAOOOOOOOOOOOඞඞඞඞඞ  sus  _(:.3 J L)_ ඞ
if __name__ == '__main__':
    G = Game()
