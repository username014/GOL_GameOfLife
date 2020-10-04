import pygame
from pygame.locals import *
import curse

class Console(UI):

    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        pass

    def draw_grid(self, screen) -> None:
        pass

    def run(self) -> None:
        screen = curses.initscr()
        curses.endwin()

class GameOfLife:
    def __init__(self, size: Tuple[int, int], randomize: bool=True, max_generations: Optional[int]=None) -> None
        self.rows, self.cols = size
        self.prev_generation = self.create_grid()
        self.curr_generation = self.create_grid(randomize=randomize)
        self.max_generations = max_generations
        self.generations = 1


def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (0, y), (self.width, y))

   def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_lines()
            draw_grid()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


if __name__ == '__main__':
    game = GameOfLife(320, 240, 20)
    game.run()


def create_grid(self, randomize: bool = False) -> Grid:
    pass

def get_neighbours(self, cell: Cell) -> Cells:
    pass

def get_next_generation(self) -> Grid:
    pass

def step(self) -> None:
    pass


@property
def is_max_generations_exceeded(self) -> bool:
    pass


@property
def is_changing(self) -> bool:
    pass


@staticmethod
def from_file(filename: pathlib.Path) -> 'GameOfLife':
    pass


def save(filename: pathlib.Path) -> None:
    pass