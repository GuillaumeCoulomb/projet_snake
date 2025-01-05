import pygame
import argparse
import random
import abc

# Récupération de la taille de la fenêtre
def windowsize():
    parser = argparse.ArgumentParser(description='Window size with numbers of tiles.')
    parser.add_argument('-L', help="largeur", type=int, default=400)
    parser.add_argument('-W', help="longueur", type=int, default=400)
    args = parser.parse_args()
    
    #checking arguments
    # if not re.match(r'#[0-9A-Fa-f]{6}$',args.fruit_color):
    #     raise ColorError(color_fruit,'--fruit-color')
    
    return (args.W, args.L)


# Classe Tile
class Tile:
    def __init__(self, row, column, color, size):
        self.row = row
        self.column = column
        self.color = color
        self.size = size

    def draw(self, screen):
        rect = pygame.Rect(self.column * self.size, self.row * self.size, self.size, self.size)
        pygame.draw.rect(screen, self.color, rect)

# Classes abstraites Subject et Observer



class Observer(abc.ABC):

    def __init__(self) -> None:
        super().__init__()

    def notify_object_eaten(self, obj: "Fruit") -> None:
        pass

    def notify_object_moved(self, obj: "A") -> None:
        pass
    def notify_collision(self, obj: "A") -> None:
        pass


class Subject(abc.ABC):

    def __init__(self) -> None:
        super().__init__()
        self._observers: list[Observer] = []

    @property
    def observers(self) -> list[Observer]:
        return self._observers

    def attach_obs(self, obs: Observer) -> None:
        print(f"Attach {obs} as observer of {self}.")
        self._observers.append(obs)

    def detach_obs(self, obs: Observer) -> None:
        print(f"Detach observer {obs} from {self}.")
        self._observers.remove(obs)


# Classe Board
class Board(Observer):
    def __init__(self, size):
        self.objects = []
        self.size = size
        self.width = size[0]
        self.length = size[1]

    def add_object(self, game_object):
        self.objects.append(game_object)
        

    def draw(self, screen):
        screen.fill((0, 0, 0))
        for obj in self.objects:
            for tile in obj.tiles:
                tile.draw(screen)

   
        

# Classe GameObject
class GameObject(Subject,Observer):
    def __init__(self):
        super().__init__()

    @property
    @abc.abstractmethod
    def tiles(self):
        pass

    def __contains__(obj1,obj2):
        for pos in obj1.position:
            if pos in obj2:
                return True


# Classe Checkerboard
class Checkerboard(GameObject):
    def __init__(self, size):
        
        super().__init__()
        self.width = size[0]
        self.length = size[1]
        self.tile_size = 20
        self.colors = [(0, 0, 0), (255, 255, 255)]

    @property
    def tiles(self):
        for row in range(self.length // self.tile_size):
            for column in range(self.width // self.tile_size):
                color = self.colors[(1 + (-1) ** (row + column)) // 2]
                yield Tile(row, column, color, self.tile_size)

# Classe Snake
class Snake(GameObject,Observer):
    def __init__(self):
        super().__init__()
        self.position = [[10, 5], [10, 6], [10, 7]]
        self.tete = [10, 7]
        self.vitesse = 2
        self.color = (0, 255, 0)
        self.tile_size = 20
        self.score=0
        self.direction = [0, 1]
        self.eaten=False

    def controle(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != [1, 0]:
                    self.direction = [-1, 0]
                elif event.key == pygame.K_DOWN and self.direction != [-1, 0]:
                    self.direction = [1, 0]
                elif event.key == pygame.K_RIGHT and self.direction != [0, -1]:
                    self.direction = [0, 1]
                elif event.key == pygame.K_LEFT and self.direction != [0, 1]:
                    self.direction = [0, -1]
                elif event.key == pygame.K_f:
                    pygame.quit()
                    quit()

    def deplacement(self):
        
        if self.eaten==True:
            self.eaten=False
        else:
            self.position.pop(0)
        self.tete = [self.tete[0] + self.direction[0], self.tete[1] + self.direction[1]]
        self.position.append(self.tete)
        
        
        if self.tete in self.position[0:-1]:
            pygame.quit()
            quit()

    def notify_object_eaten(self, obj: "Fruit"):
        self.score=1+self.score
        self.vitesse=self.vitesse+1
        self.eaten=True
        



    @property
    def tiles(self):
        for pos in self.position:
            yield Tile(pos[0], pos[1], self.color, self.tile_size)


# Classe Fruit
class Fruit(GameObject, Subject):
    def __init__(self, checkerboard_size, tile_size=20):
        super().__init__()  # Call the parent constructors correctly
        self.tile_size = tile_size
        self.color = (255, 0, 0)
        self.position = [10, 10]  # Initial position of the fruit
        self.size = checkerboard_size  # Save the size for generating positions

    def new_position(self):
        self.position = [
            random.randint(0, self.size[1] // self.tile_size - 1),
            random.randint(0, self.size[0] // self.tile_size - 1),
        ]
        

    def update(self, snake) -> None:
        if self.position in snake.position:
            self.new_position()
            #snake.notify_object_eaten(self)
            for obs in self.observers:
                obs.notify_object_eaten(self)
                

    @property
    def tiles(self):
        return [Tile(self.position[0], self.position[1], self.color, self.tile_size)]


class GameOver():
    def __init__(self):
        self.name="gameover"

        self.coord=[]
        for i in range(checkerboard.length):
            self.bord.append([i,0])
            self.bord.append([i+checkerboard.width])
        for j in range(checkerboard.width):
            self.bord.append([0,j])
            self.bord.append([checkerboard.length,j])
        

    def bord_touche(self,snake,checkerboard):
        if snake.tete in self.bord:
            pygame.quit()
            quit()


# Fonction principale
def launch_snake():
    pygame.init()
    size = windowsize()
    screen = pygame.display.set_mode(size)
    board = Board(size)
    checkerboard = Checkerboard(size)
    snake = Snake()
    fruit = Fruit(size)
    fruit.attach_obs(snake)
    clock = pygame.time.Clock()

    board.add_object(checkerboard)
    board.add_object(snake)
    board.add_object(fruit)

    while True:
        clock.tick(snake.vitesse)
        snake.controle()
        snake.deplacement()
        fruit.update(snake)
        board.draw(screen)
        pygame.display.set_caption("score : "+str(snake.score))
        pygame.display.update()




"""Snake package"""

class SnakeException(Exception):
    def __init__(self,message:str)-> None:
        super().__init__(message)
    
class SnakeError(SnakeException):
    def __init__(self,message)-> None:
        super.__init__(message)

class IntRangeError(SnakeError):
    def __init__(self,name:str,value:int,Vmax:int)->None:
        super().__init__(f"Value {value} of {name}")
