import pygame
import argparse
import random
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
        self.vitesse=2
        

    def deplacement(self,command,fruit):
        if fruit.mange !=1 :
           self.position.pop(0)


        self.tete=[self.tete[0]+command.direction[0],self.tete[1]+command.direction[1]]
        self.position.append(self.tete)
        
    def collision(self):
        if self.tete in self.position[0:-1:1]:
            pygame.quit()    
            
            

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
                
                if event.key == pygame.K_UP and self.direction !=[1,0]:
                    self.direction=[-1,0]   
                if event.key == pygame.K_DOWN and self.direction != [-1,0]:
                    self.direction=[1,0]
                
                if event.key == pygame.K_RIGHT and self.direction != [0,-1]:
                    self.direction=[0,1]
                if event.key == pygame.K_LEFT and self.direction !=[0,1]:
                    self.direction=[0,-1]
                if event.key == pygame.K_f:
                    pygame.quit()



class Fruit:
    def __init__(self):
        self.position=[5,5]
        self.mange=0
        self.k=0
        self.score=0
 
    def grandit(self,snake,checkerboard):
        if self.position==snake.tete:
            self.mange=1
            snake.vitesse=snake.vitesse+1
            self.position=[random.randint(0,checkerboard.width//20),random.randint(0,checkerboard.length//20)]
            self.score=self.score+1
            
        else :
            self.mange=0

    def nouveau(self,checkerboard,R):
        if self.mange==1:
            
            #self.position=[self.position[0]+1,self.position[1]+1]
            random.seed()
            #self.position=[random.randint(0,10),random.randint(0,10)]

        
            self.mange=0
        

    def draw(self,screen):
        width=20
        height=20

        rect = pygame.Rect( 20*self.position[1],20*self.position[0], width, height)
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

    vitesse=0
   
    
    while True:

        clock.tick(snake.vitesse)

        

        # for event in pygame.event.get():
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_f:
        #             pygame.quit()
        
        command.controle()
        
        
        snake.deplacement(command,fruit)
        fruit.grandit(snake,checkerboard)
        #fruit.nouveau(checkerboard,R)
        snake.collision()
        

        checkerboard.draw(screen)
        fruit.draw(screen)
        snake.draw(screen)
        pygame.display.set_caption("score : "+str(fruit.score) +"fruit"+str(fruit.position)+"tete"+str(snake.tete))
        pygame.display.update()
             
        

        
        