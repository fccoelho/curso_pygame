import pygame
from pygame.locals import (KEYDOWN,
                           KEYUP,
                           K_LEFT,
                           K_RIGHT,
                           QUIT,
K_m, K_LEFTBRACKET, K_RIGHTBRACKET,
                           K_ESCAPE, K_UP, K_DOWN, K_RCTRL, K_LCTRL
                           )
from fundo import Fundo
from elementos import ElementoSprite
import random
from  time import sleep


class Jogo:
    def __init__(self, size=(1000, 1000), fullscreen=False):
        self.elementos = {}
        pygame.init()
        flags = pygame.DOUBLEBUF
        if fullscreen:
            flags |= pygame.FULLSCREEN
        self.tela = pygame.display.set_mode(size, flags=flags, depth=16)
        self.fundo = Fundo()
        self.jogador = None
        self.interval = 0
        self.nivel = 0
        pygame.font.init()
        self.fonte = pygame.font.SysFont('bitstreamverasans', 42)
        self.fonte2 = pygame.font.SysFont('bitstreamverasans', 80)
        pygame.mixer.music.load('sons/space-syndrome.wav')
        self.explosão = pygame.mixer.Sound('sons/retro-explosion-02.wav')
        pygame.mixer.music.play(-1)
        self.music = True
        self.screen_size = self.tela.get_size()
        pygame.mouse.set_visible(0)
        pygame.display.set_caption('Corona Shooter')
        self.run = True
        self.go = False

    def liga_desliga_musica(self):
        if self.music:
            pygame.mixer.music.pause()
            self.music = False
        else:
            pygame.mixer.music.unpause()
            self.music = True

    def ajusta_volume(self, m):
        volume = pygame.mixer.music.get_volume()
        volume *= m
        if volume > 1:
            volume = 1
        if volume < 0.1:
            volume = 0.1
        pygame.mixer.music.set_volume(volume)

    def escreve_placar(self):
        vidas = self.fonte.render(f'vidas: {self.jogador.get_lives()*"❤"}', 1, (255, 255, 0), (0, 0, 0))
        score = self.fonte.render(f'Score: {self.jogador.pontos}', 1, (255, 255, 0), (0, 0, 0))
        self.tela.blit(vidas, (30, 30))
        self.tela.blit(score, (self.screen_size[0] - 300, 30))

    def game_over(self):
        gameover = self.fonte2.render("GAME OVER!", 1, (255, 255, 0), (0, 0, 0))
        self.tela.blit(gameover, (self.screen_size[0]//4, self.screen_size[1]//2))

    def manutenção(self):
        r = random.randint(0, 100)
        x = random.randint(1, self.screen_size[0])
        virii = self.elementos["virii"]
        if r > (10 * len(virii)):
            enemy = Virus([0, 0])
            size = enemy.get_size()
            enemy.set_pos([min(max(x, size[0] / 2), self.screen_size[0] - size[0] / 2), size[1] / 2])
            colisores = pygame.sprite.spritecollide(enemy, virii, False)
            if colisores:
                return
            self.elementos["virii"].add(enemy)

    def muda_nivel(self):
        xp = self.jogador.get_pontos()
        if xp > 10 and self.level == 0:
            self.fundo = Fundo("tile2.png")
            self.nivel = 1
            self.jogador.set_lives(self.jogador.get_lives() + 3)
        elif xp > 50 and self.level == 1:
            self.fundo = Fundo("tile3.png")
            self.nivel = 2
            self.jogador.set_lives(self.player.get_lives() + 6)

    def atualiza_elementos(self, dt):
        self.fundo.update(dt)
        for v in self.elementos.values():
            v.update(dt)

    def desenha_elementos(self):
        self.fundo.draw(self.tela)
        for v in self.elementos.values():
            v.draw(self.tela)

    def verifica_impactos(self, elemento, list, action):
        """
        Verifica ocorrência de colisões.
        :param elemento: Instância de RenderPlain ou seja um grupo de sprites
        :param list: lista ou grupo de sprites
        :param action: função a ser chamada no evento de colisão
        :return: lista de sprites envolvidos na colisão
        """
        if isinstance(elemento, pygame.sprite.RenderPlain):
            hitted = pygame.sprite.groupcollide(elemento, list, 1, 0)
            for v in hitted.values():
                for o in v:
                    action(o)
            return hitted

        elif isinstance(elemento, pygame.sprite.Sprite):
            if pygame.sprite.spritecollide(elemento, list, 1):
                action()
            return elemento.morto

    def ação_elemento(self):
        """
        Executa as ações dos elementos do jogo.
        :return:
        """
        self.verifica_impactos(self.jogador, self.elementos["tiros_inimigo"],
                               self.jogador.alvejado)
        if self.jogador.morto:
            pygame.mixer.Sound.play(self.explosão)
            self.go = True
            self.run = False
            return

        # Verifica se o personagem trombou em algum inimigo
        self.verifica_impactos(self.jogador, self.elementos["virii"],
                               self.jogador.colisão)
        if self.jogador.morto:
            pygame.mixer.Sound.play(self.explosão)
            self.go = True
            self.run = False
            return
        # Verifica se o personagem atingiu algum alvo.
        hitted = self.verifica_impactos(self.elementos["tiros"],
                                        self.elementos["virii"],
                                        Virus.alvejado)

        # Aumenta a pontos baseado no número de acertos:
        self.jogador.set_pontos(self.jogador.get_pontos() + len(hitted))

    def trata_eventos(self):
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            self.run = False

        if event.type in (KEYDOWN,):
            key = event.key
            if key == K_ESCAPE:
                self.run = False
            elif key in (K_LCTRL, K_RCTRL):
                self.interval = 0
                self.jogador.atira(self.elementos["tiros"])
            elif key == K_UP:
                self.jogador.accel_top()
            elif key == K_DOWN:
                self.jogador.accel_bottom()
            elif key == K_RIGHT:
                self.jogador.accel_right()
            elif key == K_LEFT:
                self.jogador.accel_left()
            elif key == K_m:
                self.liga_desliga_musica()
            elif key == K_LEFTBRACKET:
                self.ajusta_volume(0.9)
            elif key == K_RIGHTBRACKET:
                self.ajusta_volume(1.1)


        keys = pygame.key.get_pressed()
        if self.interval > 10:
            self.interval = 0
            if keys[K_RCTRL] or keys[K_LCTRL]:
                self.jogador.atira(self.elementos["tiros"])

    def loop(self):
        clock = pygame.time.Clock()
        dt = 16
        self.elementos['virii'] = pygame.sprite.RenderPlain(Virus([120, 50]))
        self.jogador = Jogador([200, 400], 5)
        self.elementos['jogador'] = pygame.sprite.RenderPlain(self.jogador)
        self.elementos['tiros'] = pygame.sprite.RenderPlain()
        self.elementos['tiros_inimigo'] = pygame.sprite.RenderPlain()
        while self.run:
            clock.tick(1000 / dt)

            self.trata_eventos()

            self.ação_elemento()
            self.manutenção()
            # Atualiza Elementos
            self.atualiza_elementos(dt)

            # Desenhe no back buffer
            self.desenha_elementos()
            if self.go:
                self.game_over()
            # texto = self.fonte.render(f"Vidas: {self.jogador.get_lives()}", True, (255, 255, 255), (0, 0, 0))
            self.escreve_placar()
            pygame.display.flip()
        sleep(2)


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

    def colisão(self):
        if self.get_lives() <= 0:
            self.kill()
        else:
            self.set_lives(self.get_lives() - 1)

    def atira(self, lista_de_tiros, image=None):
        s = list(self.get_speed())
        s[1] *= 2
        Tiro(self.get_pos(), s, image, lista_de_tiros)

    def alvejado(self):
        if self.get_lives() <= 0:
            self.kill()
        else:
            self.set_lives(self.get_lives() - 1)

    @property
    def morto(self):
        return self.get_lives() == 0

    def accel_top(self):
        speed = self.get_speed()
        self.set_speed((speed[0], speed[1] - self.acceleration[1]))

    def accel_bottom(self):
        speed = self.get_speed()
        self.set_speed((speed[0], speed[1] + self.acceleration[1]))

    def accel_left(self):
        speed = self.get_speed()
        self.set_speed((speed[0] - self.acceleration[0], speed[1]))

    def accel_right(self):
        speed = self.get_speed()
        self.set_speed((speed[0] + self.acceleration[0], speed[1]))


class Virus(Nave):
    def __init__(self, position, lives=1, speed=None, image=None, size=(100, 100)):
        if not image:
            image = "virus.png"
        super().__init__(position, lives, speed, image, size)


class Jogador(Nave):
    """
    A classe Player é uma classe derivada da classe GameObject.
       No entanto, o personagem não morre quando passa da borda, este só
    interrompe o seu movimento (vide update()).
       E possui experiência, que o fará mudar de nivel e melhorar seu tiro.
       A função get_pos() só foi redefinida para que os tiros não saissem da
    parte da frente da nave do personagem, por esta estar virada ao contrário
    das outras.
    """

    def __init__(self, position, lives=10, image=None, new_size=[83, 248]):
        if not image:
            image = "seringa.png"
        super().__init__(position, lives, [0, 0], image, new_size)
        self.pontos = 0

    def alvejado(self):
        if self.get_lives() <= 0:
            pygame.mixer.Sound.play(self.explosão)
            self.kill()
        else:
            self.set_lives(self.get_lives() - 1)
    def update(self, dt):
        move_speed = (self.speed[0] * dt / 16,
                      self.speed[1] * dt / 16)
        self.rect = self.rect.move(move_speed)

        if (self.rect.right > self.area.right):
            self.rect.right = self.area.right

        elif (self.rect.left < 0):
            self.rect.left = 0

        if (self.rect.bottom > self.area.bottom):
            self.rect.bottom = self.area.bottom

        elif (self.rect.top < 0):
            self.rect.top = 0

    def get_pos(self):
        return (self.rect.center[0], self.rect.top)

    def get_pontos(self):
        return self.pontos

    def set_pontos(self, pontos):
        self.pontos = pontos

    def atira(self, lista_de_tiros, image=None):
        l = 1
        if self.pontos > 10:
            l = 3
        if self.pontos > 50:
            l = 5

        p = self.get_pos()
        speeds = self.get_fire_speed(l)
        for s in speeds:
            Tiro(p, s, image, lista_de_tiros)

    def get_fire_speed(self, shots):
        speeds = []

        if shots <= 0:
            return speeds

        if shots == 1:
            speeds += [(0, -5)]

        if shots > 1 and shots <= 3:
            speeds += [(0, -5)]
            speeds += [(-2, -3)]
            speeds += [(2, -3)]

        if shots > 3 and shots <= 5:
            speeds += [(0, -5)]
            speeds += [(-2, -3)]
            speeds += [(2, -3)]
            speeds += [(-4, -2)]
            speeds += [(4, -2)]

        return speeds


class Tiro(ElementoSprite):
    def __init__(self, position, speed=None, image=None, list=None):
        if not image:
            image = "tiro.png"
        super().__init__(image, position, speed)
        if list is not None:
            self.add(list)


if __name__ == '__main__':
    J = Jogo(fullscreen=False)
    J.loop()
