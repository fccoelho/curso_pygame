import pygame

pygame.init()
window = pygame.display.set_mode((640,480))

while True:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        break
    pygame.display.update()

pygame.quit()
