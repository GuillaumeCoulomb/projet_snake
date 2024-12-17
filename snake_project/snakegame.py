import pygame
import argparse
import random
import abc

def windowsize(): #ask the size of the checkerboard
    parser = argparse.ArgumentParser(description='Window size with numbers of tiles.')
    parser.add_argument('-L', help="largeur", type=int, default=400)
    parser.add_argument('-W', help="longueur", type=int, default=400)
    args = parser.parse_args()
    return (args.W, args.L)

class Tile: #manage the tile drawing
    def __init__(self, row, column, color, size):
        self.row = row
        self.column = column
        self.color = color
        self.size = size

    def draw(self, screen):
        rect = pygame.Rect(self.column * self.size, self.row * self.size, self.size, self.size)
        pygame.draw.rect(screen, self.color, rect)

class GameObject(abc.ABC):
    @property
    @abc.abstractmethod
    def tiles(self):
        pass

class Checkerboard(GameObject): #manage the checkerboard
    def __init__(self, size):
        self.width = size[0]
        self.length = size[1]
        self.tile_size = 20
        self.colors = [(0, 0, 0), (255, 255, 255)] 

    @property
    def tiles(self):
        for row in range(self.length // self.tile_size):
            for column in range(self.width // self.tile_size):
                color = self.colors[(1 + (-1) ** (row + column)) // 2]
                yield Tile(row, column, color, self.tile_size) #generate the tiles of the checkerboard

class Snake(GameObject):
    def __init__(self):
        self.position = [[10, 5], [10, 6], [10, 7]] #initial position of the checkerboard
        self.tete = [10, 7]
        self.vitesse = 2
        self.color = (0, 255, 0)
        self.tile_size = 20

    def deplacement(self, command, fruit): #manage the deplacement of one tile of the snake
        if not fruit.mange: #if fruit.mange, the snake gets one more tile
            self.position.pop(0)
        self.tete = [self.tete[0] + command.direction[0], self.tete[1] + command.direction[1]]
        self.position.append(self.tete)

    def collision(self):
        if self.tete in self.position[:-1]:
            pygame.quit() #ends the game if the player loses
            quit()

    @property
    def tiles(self):
        for pos in self.position:
            yield Tile(pos[0], pos[1], self.color, self.tile_size)

class Fruit(GameObject):
    def __init__(self):
        self.position = [5, 5]
        self.mange = 0
        self.score = 0
        self.color = (255, 0, 0)
        self.tile_size = 20

    def grandit(self, snake, checkerboard):
        if self.position == snake.tete:
            self.mange = 1
            snake.vitesse += 1
            self.position = [random.randint(0,checkerboard.length// self.tile_size - 1), #generates a new position of the fruit
                             random.randint(0,checkerboard.width// self.tile_size - 1)]
            self.score += 1
        else:
            self.mange = 0

    @property
    def tiles(self):
        return [Tile(self.position[0], self.position[1], self.color, self.tile_size)]

class Board:
    def __init__(self, size):
        self.objects = []
        self.width=size[0]
        self.length=size[1]

    def add_object(self, game_object):
        self.objects.append(game_object)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        for obj in self.objects:
            for tile in obj.tiles:
                tile.draw(screen)

    def interactions(self):
        snake = next(obj for obj in self.objects if isinstance(obj, Snake))
        fruit = next(obj for obj in self.objects if isinstance(obj, Fruit))
        checkerboard= next(obj for obj in self.objects if isinstance(obj, Checkerboard))
        fruit.grandit(snake=snake,checkerboard=checkerboard)
        snake.collision()

class Command:
    def __init__(self):
        self.direction = [0, 1]

    def controle(self): #gets information from the keys of the computer
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

def launch_snake():
    pygame.init()
    size = windowsize()
    screen = pygame.display.set_mode(size)
    board = Board(size)
    snake = Snake()
    fruit = Fruit()
    checkerboard = Checkerboard(size)
    command = Command()
    clock = pygame.time.Clock()

    board.add_object(checkerboard)
    board.add_object(snake)
    board.add_object(fruit)

    print("Partie lancée")

    while True:
        clock.tick(snake.vitesse)
        command.controle()
        snake.deplacement(command, fruit)
        board.interactions()
        board.draw(screen)
        pygame.display.set_caption(f"Score : {fruit.score}")
        pygame.display.update()
