import pygame
import argparse

#fonction pour demander dimensions



#liste position du serpent :



#fonction pour lancer snake



class Checkerboard:

    def __init__(self):
        parser = argparse.ArgumentParser(description='demander dimensions')
        # parser.add_argument('-D', type=tuple, help="tuple dimensions")
        parser.add_argument('-W', help="largeur", type=int)
        parser.add_argument('-L', help="longueur", type=int)
        args=parser.parse_args()
        
        self.width=args.W
        self.length=args.L

        
    
    def draw(self, screen):
        dimensions=[self.width,self.length]
        color = [(0,0,0),(255, 255, 255)] # blue
        
        
        for i in range(dimensions[0]//20):
            for j in range(dimensions[1]//20):

                left=i*20
                top=j*20
                width=20
                height=20
                ind=(1+(-1)**(i+j))//2 #alternance noir blanc

                rect = pygame.Rect(left, top, width, height)
                pygame.draw.rect(screen, color[ind], rect)

class Snake:
    def __init__(self):
        self.name="serpent"
        self.position=[[10,5],[10,6],[10,7]]
        self.tete=[10,7]
        self.grandit=0

    def deplacement(self,command,fruit):
        if self.tete!=fruit.position:
           self.position.pop(0)


        self.tete=[self.tete[0]+command.direction[0],self.tete[1]+command.direction[1]]
        self.position.append(self.tete)
        self.grandit=0
        

            

    def draw(self,screen):
        for elt in self.position:
            left=elt[1]*20
            top=elt[0]*20
            width=20
            height=20

            rect = pygame.Rect(left, top, width, height)
            pygame.draw.rect(screen, (0,255,0), rect)

class Command:
    def __init__(self):
        self.name="commande"
        self.direction=[0,1]


    def controle(self):
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_UP:
                    self.direction=[-1,0]   
                if event.key == pygame.K_DOWN:
                    self.direction=[1,0]
                
                if event.key == pygame.K_RIGHT:
                    self.direction=[0,1]
                if event.key == pygame.K_LEFT:
                    self.direction=[0,-1]
                if event.key == pygame.K_f:
                    pygame.quit()

class Fruit:
    def __init__(self):
        self.position=[20,20]
 

    def draw(self,screen):
        width=20
        height=20

        rect = pygame.Rect(20*self.position[0], 20*self.position[1], width, height)
        pygame.draw.rect(screen, (255,0,0), rect)


def launch_snake():

    pygame.init()

    checkerboard=Checkerboard()   
    snake=Snake()
    command=Command()
    fruit=Fruit()

    clock = pygame.time.Clock()

    screen=pygame.display.set_mode( (checkerboard.width,checkerboard.length) )

    print("partie lancée")



    while True:

        clock.tick(10)

        # for event in pygame.event.get():
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_f:
        #             pygame.quit()

        command.controle()
        #fruit.mange(snake)

        snake.deplacement(command,fruit)
        
        checkerboard.draw(screen)
        snake.draw(screen)
        fruit.draw(screen)
             
        pygame.display.update()

        
        