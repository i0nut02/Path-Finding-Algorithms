import pygame
from button import Button
from algorithms import Algoriths
from spot import Spot

class Main:

    def __init__(self):
        self.WIDTH = 800
        self.WHITE = (255, 255, 255)
        self.GREY = (128, 128, 128)
        self.WIN = pygame.display.set_mode((self.WIDTH, self.WIDTH + 50))
        pygame.display.set_caption("Path Finding Algorithms")
    
        self.algorithm_button = Button("A* algorithm ", (1, 801), (319, 50), font=40)
        self.run_button = Button("Run", (321, 801), (100, 50), font=40)
        self.reset_all_button = Button("Reset all", (422, 801), (180, 50), font=40)
        self.reset_path_button = Button("Reset path", (603, 801), (196, 50), font=40)
        self.run()

    
    def run(self):
        ROWS = 50
        grid = self.make_grid(ROWS)

        start = None
        end = None
        
        run = True
        algorithm = Algoriths()

        while run:
            self.draw(grid, ROWS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                

                if self.algorithm_button.click(event):
                    algorithm.change_algorithm()
                    self.algorithm_button.change_text(algorithm.algorithm_name, (319, 50))


                elif self.run_button.click(event):
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    algorithm.run(lambda: self.draw(grid, ROWS), grid, start, end)
                

                elif self.reset_all_button.click(event):
                    start = None
                    end = None
                    grid = self.make_grid(ROWS)
                

                elif self.reset_path_button.click(event):
                    for row in grid:
                        for spot in row:
                            if not (spot.is_start() or spot.is_end() or spot.is_barrier()):
                                spot.reset()


                elif pygame.mouse.get_pressed()[0]: # LEFT
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_clicked_pos(pos, ROWS)
                    if row >= 50 or col >= 50:
                        continue
                    
                    spot = grid[row][col]

                    if not start and spot != end:
                        start = spot
                        start.make_start()

                    elif not end and spot != start:
                        end = spot
                        end.make_end()

                    elif spot != end and spot != start:
                        spot.make_barrier()

                    
                elif pygame.mouse.get_pressed()[2]: # RIGHT
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_clicked_pos(pos, ROWS)

                    spot = grid[row][col]
                    spot.reset()
                    if spot == start:
                        start = None
                    elif spot == end:
                        end = None



    def make_grid(self, rows):
        grid = []
        gap = self.WIDTH // rows
        for i in range(rows):
            grid.append([])
            for j in range(rows):
                spot = Spot(i, j, gap, rows)
                grid[i].append(spot)

        return grid


    def draw(self, grid, rows):
        self.WIN.fill(self.WHITE)

        self.algorithm_button.show(self.WIN)
        self.run_button.show(self.WIN)
        self.reset_all_button.show(self.WIN)
        self.reset_path_button.show(self.WIN)

        for row in grid:
            for spot in row:
                spot.draw(self.WIN)

        self.draw_grid(rows)
        pygame.display.update()
        pass

    
    def draw_grid(self, rows):
        gap = self.WIDTH // rows
        for i in range(rows):
            pygame.draw.line(self.WIN, self.GREY, (0, i * gap), (self.WIDTH, i * gap))
            for j in range(rows):
                pygame.draw.line(self.WIN, self.GREY, (j * gap, 0), (j * gap, self.WIDTH))
        pass
            
    def get_clicked_pos(self, pos, rows):
        gap = self.WIDTH // rows
        y, x = pos

        row = y // gap
        col = x // gap

        return row, col
    
Main()