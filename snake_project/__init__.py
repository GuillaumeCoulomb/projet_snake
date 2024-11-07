import pygame
import sys

import pygame


import argparse

# def args():
#     parser = argparse.ArgumentParser(description='Some description.')
#     parser.add_argument('-W', "--width", default=400, help="screen width", type=int)
#     parser.add_argument('-H', "--high", default=300, help="screen high", type=int)
#     args = parser.parse_args()
    
#     return args



def snake():

    pygame.init()

    screen = pygame.display.set_mode( (400,300) )

    clock = pygame.time.Clock()

    while True:

        clock.tick(1)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    return True

        screen.fill( (0, 255, 0) )


        pygame.display.update()


    pygame.quit()