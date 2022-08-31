from queue import PriorityQueue
from queue import Queue
import pygame

class Algoriths:

    def __init__(self) :
        self.algorithm_name = "A* algorithm"
        self.algorithm = self.astar_algorithm

    def h(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        
        return abs(x1 - x2) + abs(y1 - y2)

    def astar_algorithm(self, draw, grid, start, end):
        count = 0
        open_set = PriorityQueue() 
        open_set.put((0, count, start))
        came_from = {}
        g_score = {spot: float("inf") for row in grid for spot in row}
        g_score[start] = 0
        f_score = {spot: float("inf") for row in grid for spot in row}
        f_score[start] = self.h(start.get_pos(), end.get_pos())

        open_set_hash = {start}

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = open_set.get()[2]
            open_set_hash.remove(current)

            if current == end:
                self.reconstruct_path(came_from, end, draw, start)
                end.make_end()
                return True

            for neighbor in current.neighbors:
                temp_g_score = g_score[current] + 1

                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + self.h(neighbor.get_pos(), end.get_pos())
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        if neighbor != end:
                            neighbor.make_open()

            draw()

            if current != start:
                current.make_closed()

        return False

    
    def reconstruct_path(self, came_from, current, draw, start):
        while current != start:
            current = came_from[current]
            if current != start:
                current.make_path()
                draw()
            
    def dijkstra_algorithm(self, draw, grid, start, end):
        open_set = Queue()
        open_set.put(start)
        came_from = {}
        g_score = {spot: float("inf") for row in grid for spot in row}
        g_score[start] = 0

        open_set_hash = {start}

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            
            current = open_set.get()
            open_set_hash.remove(current)

            if current == end:
                self.reconstruct_path(came_from, end, draw, start)
                end.make_end()
                return True
            
            for neighbor in current.neighbors:
                temp_g_score = g_score[current] + 1

                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score

                    if neighbor not in open_set_hash:
                        open_set.put(neighbor)
                        open_set_hash.add(neighbor)
                        if neighbor != end:
                            neighbor.make_open()
                    
            draw()

            if current != start:
                current.make_closed()
        return False
    
    def run(self, draw, grid, start, end):
        self.algorithm(draw, grid, start, end)
    
    def change_algorithm(self):
        if self.algorithm_name == "A* algorithm":
            self.algorithm_name = "Dijkstra algorithm"
            self.algorithm = self.dijkstra_algorithm
        else:
            self.algorithm_name = "A* algorithm"
            self.algorithm = self.astar_algorithm

        return self.algorithm_name 