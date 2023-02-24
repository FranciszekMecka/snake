import pygame
from sys import exit
import random

pygame.init()
pygame.font.init()

class Tile:
    def __init__(self, x: int, y: int, size: int, color: str) -> None:
        self.pos_x: int = x
        self.pos_y: int = y
        self.color: str = color
        self.size: int = size
        self.surface = pygame.Surface((size, size))
        self.surface.fill(color)

class Background:
    def __init__(self, size: int, color: str) -> None:
        self.Tiles = []
        self.size = size
        self.color = color
        self.generate_tiles()

    def generate_tiles(self):
        j = 0
        i = 0
        while j < 600: # screen height
            if int(i/self.size)%2 == 0:
                if int(j/self.size)%2 == 0:
                    self.Tiles.append(Tile(i, j, self.size, 'gray10'))
                else:
                    self.Tiles.append(Tile(i, j, self.size, self.color))
            else:
                if int(j/self.size)%2 == 0:
                    self.Tiles.append(Tile(i, j, self.size, self.color))
                else:
                    self.Tiles.append(Tile(i, j, self.size, 'gray10'))
            i += self.size
            if i == 800: # screen width
                i = 0
                j += self.size

    def print_bg(self, screen):
        for tile in self.Tiles:
            screen.blit(tile.surface, (tile.pos_x, tile.pos_y))
        
class Snake:
    def __init__(self, length: int):
        self.body: Tile = []
        self.length = length
        self.create_body()
    
    def create_body(self):
        for x in range(self.length):
            self.body.append(Tile(400 + x * 40, 400, 40, 'Green'))

    def print_snake(self, screen):
        for x in self.body:
            screen.blit(x.surface, (x.pos_x, x.pos_y))

    def move_snake(self, direction):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].pos_x = self.body[i - 1].pos_x
            self.body[i].pos_y = self.body[i - 1].pos_y
        self.body[0].pos_x += direction[0]
        self.body[0].pos_y += direction[1]
        for i in range(1, len(self.body) - 1):
            if (self.body[i].pos_x == self.body[0].pos_x
                and self.body[i].pos_y == self.body[0].pos_y):
                self.length = 1
                self.body = self.body[:1]
                break

class Fruit:
    def __init__(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.tile = Tile(200, 600, 40, 'red')

    def print_fruit(self, screen):
        screen.blit(self.tile.surface, (self.pos_x, self.pos_y))

    def colision(self, snake: Snake) -> bool:
        if (self.pos_x == snake.body[0].pos_x
             and self.pos_y == snake.body[0].pos_y):
            return True
        return False

class Game:
    UP = (0, -40)
    DOWN = (0, 40)
    LEFT = (-40, 0)
    RIGHT = (40, 0)
    direction = (-40, 0)
    my_font = pygame.font.SysFont('Arial', 30)
    
    def __init__(self) -> None:
        self.fruits = [Fruit(random.randint(19*40), random.randint(14*40))]
    def controlls(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.direction = self.UP
                if event.key == pygame.K_DOWN:
                    self.direction = self.DOWN
                if event.key == pygame.K_RIGHT:
                    self.direction = self.RIGHT
                if event.key == pygame.K_LEFT:
                    self.direction = self.LEFT

    def fruit_controller(self, screen, snake: Snake):
        for x in self.fruits:
            x.print_fruit(screen)
            if(x.colision(snake)):
                self.fruits.remove(x)
                last_body = snake.body[-1]
                snake.length += 1
                # this needs to be done better
                snake.body.append(Tile(last_body.pos_x, last_body.pos_y, 40, 'Green'))
                self.fruits.append(Fruit(random.randint(0,19) * 40, random.randint(0,14) * 40))
    def print_score(self, snake: Snake, screen):
        text_surface = self.my_font.render(f'Score: {snake.length}', False, (255, 255, 255))
        screen.blit(text_surface, (0,0))


screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Snake')
events = pygame.event.get()
clock = pygame.time.Clock()

b = Background(40, 'gray13')
s = Snake(5)
g = Game()

timer = 0

while True:
    g.controlls()
    b.print_bg(screen)
    g.fruit_controller(screen, s)
    s.print_snake(screen)
    s.move_snake(g.direction)
    g.print_score(s, screen)
    pygame.display.update()
    clock.tick(10)