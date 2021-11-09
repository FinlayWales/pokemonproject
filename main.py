import pygame
from pygame.locals import *
import sys
import json
import math
from imports.functions import *
from battle.showdownwrapper import *

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
pygame.font.init()
thefont = pygame.font.SysFont('Arial', 20)

DISPLAYSURF = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Pokemon ???")


simulate_battle()

FPS = pygame.time.Clock()

while True:
    
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            
    FPS.tick(60)

