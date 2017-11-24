import pygame, time
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Pygame Keyboard test")
pygame.mouse.set_visible(0)

while True:
    print ("Doing function")

    for event in pygame.event.get():
        if (event.type == KEYUP) or (event.type == KEYDOWN):
            print("Key pressed")
    time.sleep(0.3)
