import pygame
from sys import exit

class Tile:
    def __init__(self, x: int, y: int, size: int, color: str) -> None:
        self.pos_x = x
        self.pos_y = y
        self.color = color
        self.size = size
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
                    self.Tiles.append(Tile(i, j, self.size, 'Grey'))
                else:
                    self.Tiles.append(Tile(i, j, self.size, self.color))
            else:
                if int(j/self.size)%2 == 0:
                    self.Tiles.append(Tile(i, j, self.size, self.color))
                else:
                    self.Tiles.append(Tile(i, j, self.size, 'Grey'))
            i += self.size
            if i == 800: # screen width
                i = 0
                j += self.size

    def print_bg(self, screen):
        for tile in self.Tiles:
            screen.blit(tile.surface, (tile.pos_x, tile.pos_y))
        
class Snake:
    def __init__(self, length: int):
        self.body = []
        self.length = length
        self.create_body()
    
    def create_body(self):
        for x in range(self.length):
            self.body.append(Tile(120 + x * 40, 120, 40, 'Green'))

    def print_snake(self, screen):
        for x in self.body:
            screen.blit(x.surface, (x.pos_x, x.pos_y))


pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Snake')
events = pygame.event.get()
clock = pygame.time.Clock()
b = Background(40, 'Blue')
s = Snake(5)

while True:
    for event in pygame.event.get():
        #print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    b.print_bg(screen)
    s.print_snake(screen)

    pygame.display.update()
    clock.tick(60)