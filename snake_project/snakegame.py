import pygame
import argparse


def ask_dimensions():
    parser = argparse.ArgumentParser(description='demander dimensions')
    # parser.add_argument('-D', type=tuple, help="tuple dimensions")
    parser.add_argument('-W', help="largeur", type=int)
    parser.add_argument('-L', help="longueur", type=int)
    args=parser.parse_args()
    


    return(args.W,args.L)


def launch_snake():
       
    dimensions=ask_dimensions()

    print("partie lancée")

    pygame.init()

    screen = pygame.display.set_mode( dimensions )

    clock = pygame.time.Clock()

    while True:

        clock.tick(1)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    pygame.quit()

        screen.fill( (0, 255, 0) )


        #drawing cherckerboard :

        color = [(0,0,0),(255, 255, 255)] # blue
        for i in range(dimensions[0]//20):
            for j in range(dimensions[1]//20):

                left=i*20
                top=j*20
                width=20
                height=20
                ind=(1+(-1)**(i+j))//2

                rect = pygame.Rect(left, top, width, height)
                pygame.draw.rect(screen, color[ind], rect)

        pygame.display.update()