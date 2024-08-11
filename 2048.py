import tkinter as tk
import random

class Game2048:
    def __init__(self, master):
        self.master = master
        self.master.title('2048 Game')
        self.grid_size = 4
        self.cell_size = 100
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.setup_game()
        self.create_widgets()

    def setup_game(self):
        self.add_new_tile()
        self.add_new_tile()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.master, width=self.grid_size*self.cell_size, height=self.grid_size*self.cell_size, bg='white')
        self.canvas.pack()
        self.update_grid_display()

        self.master.bind("<Key>", self.key_handler)

    def update_grid_display(self):
        self.canvas.delete("all")
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                value = self.grid[i][j]
                if value != 0:
                    self.canvas.create_rectangle(j*self.cell_size, i*self.cell_size, 
                                                (j+1)*self.cell_size, (i+1)*self.cell_size, fill="lightgray")
                    self.canvas.create_text(j*self.cell_size+self.cell_size//2, i*self.cell_size+self.cell_size//2, 
                                            text=str(value), font=("Helvetica", 24), fill="black")

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = random.choice([2, 4])

    def compress(self, grid):
        new_grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        for i in range(self.grid_size):
            position = 0
            for j in range(self.grid_size):
                if grid[i][j] != 0:
                    new_grid[i][position] = grid[i][j]
                    position += 1
        return new_grid

    def merge(self, grid):
        for i in range(self.grid_size):
            for j in range(self.grid_size - 1):
                if grid[i][j] == grid[i][j + 1] and grid[i][j] != 0:
                    grid[i][j] *= 2
                    grid[i][j + 1] = 0
        return grid

    def reverse(self, grid):
        new_grid = []
        for i in range(self.grid_size):
            new_grid.append(list(reversed(grid[i])))
        return new_grid


    def transpose(self, grid):
        new_grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                new_grid[i][j] = grid[j][i]
        return new_grid

    def move_tiles(self, direction):
        if direction == 'Left':
            self.grid = self.compress(self.grid)
            self.grid = self.merge(self.grid)
            self.grid = self.compress(self.grid)

        elif direction == 'Right':
            self.grid = self.reverse(self.grid)
            self.grid = self.compress(self.grid)
            self.grid = self.merge(self.grid)
            self.grid = self.compress(self.grid)
            self.grid = self.reverse(self.grid)

        elif direction == 'Up':
            self.grid = self.transpose(self.grid)
            self.grid = self.compress(self.grid)
            self.grid = self.merge(self.grid)
            self.grid = self.compress(self.grid)
            self.grid = self.transpose(self.grid)

        elif direction == 'Down':
            self.grid = self.transpose(self.grid)
            self.grid = self.reverse(self.grid)
            self.grid = self.compress(self.grid)
            self.grid = self.merge(self.grid)
            self.grid = self.compress(self.grid)
            self.grid = self.reverse(self.grid)
            self.grid = self.transpose(self.grid)

    def check_game_over(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] == 0:
                    return False
                if i < self.grid_size - 1 and self.grid[i][j] == self.grid[i + 1][j]:
                    return False
                if j < self.grid_size - 1 and self.grid[i][j] == self.grid[i][j + 1]:
                    return False
        return True

    def game_over(self):
        self.canvas.create_text(self.grid_size*self.cell_size//2, self.grid_size*self.cell_size//2, 
                                text="Game Over", font=("Helvetica", 36), fill="red")

    def key_handler(self, event):
        key = event.keysym
        if key in ('Up', 'Down', 'Left', 'Right'):
            previous_grid = [row[:] for row in self.grid]
            self.move_tiles(key)
            if self.grid != previous_grid:
                self.add_new_tile()
            self.update_grid_display()
            if self.check_game_over():
                self.game_over()

if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()