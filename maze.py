from cell import Cell
import time, random

class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win = None,
        seed = None,
    ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._seed = seed

        if seed != None:
            random.seed(seed)

        self._cells = []
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
        self._reset_cells_visited() 

    def _create_cells(self):
        for i in range(self._num_cols):
            self._cells.append([])
            for j in range(self._num_rows):
                self._cells[i].append(Cell(self._win))
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        x1 = self._x1 + i*self._cell_size_x
        y1 = self._y1 + j*self._cell_size_y
        x2 = self._x1 + (i+1)*self._cell_size_x
        y2 = self._y1 + (j+1)*self._cell_size_y        
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(.05)

    def _break_entrance_and_exit(self):
        entrance_col = 0
        entrance_row = 0
        exit_col = self._num_cols - 1
        exit_row = self._num_rows - 1

        self._cells[entrance_col][entrance_row].has_top_wall = False
        self._draw_cell(entrance_col, entrance_row)
        self._cells[exit_col][exit_row].has_bottom_wall = False
        self._draw_cell(exit_col, exit_row)

    
    def _break_walls_r(self, i, j):
        if 0 <= i < self._num_cols and 0 <= j < self._num_rows:
            self._cells[i][j].visited = True

        while True:
            to_visit = []

            #above
            if j > 0 and self._cells[i][j-1].visited == False:
                to_visit.append((i, j-1))

            #below
            if j < self._num_rows - 1 and self._cells[i][j+1].visited == False:
                to_visit.append((i, j+1))

             #left
            if i > 0 and self._cells[i-1][j].visited == False:
               to_visit.append((i-1, j))

              #right
            if i < self._num_cols - 1 and self._cells[i+1][j].visited == False:
               to_visit.append((i+1, j))

            if len(to_visit) == 0:
                self._draw_cell(i, j)
                return

            r = random.randint(0, len(to_visit)-1)

            cell = to_visit[r]

            #same row
            #right
            if i + 1 == cell[0]:
                    self._cells[i][j].has_right_wall = False
                    self._cells[cell[0]][cell[1]].has_left_wall = False
            #left
            if i - 1 == cell[0]:        
                    self._cells[i][j].has_left_wall = False
                    self._cells[cell[0]][cell[1]].has_right_wall = False
            #same column
            #above
            if j + 1 == cell[1]:
                    self._cells[i][j].has_bottom_wall = False
                    self._cells[cell[0]][cell[1]].has_top_wall = False
            #below
            if j - 1 == cell[1]:
                    self._cells[i][j].has_top_wall = False
                    self._cells[cell[0]][cell[1]].has_bottom_wall = False                    
            
            self._break_walls_r(cell[0], cell[1])

    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False

    def solve(self):
         return self._solve_r(0,0)
    
    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if i == self._num_cols - 1 and j == self._num_rows - 1:
             return True
        
        #above
        if j > 0 and self._cells[i][j].has_top_wall == False and self._cells[i][j-1].visited == False:        
            self._cells[i][j].draw_move(self._cells[i][j-1], False)
            if self._solve_r(i, j-1):
                 return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j-1], True)

        #below
        if j < self._num_rows - 1 and self._cells[i][j].has_bottom_wall == False and self._cells[i][j+1].visited == False:
            self._cells[i][j].draw_move(self._cells[i][j+1], False)
            if self._solve_r(i, j+1):
                 return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j+1], True)

        #left
        if i > 0 and self._cells[i][j].has_left_wall == False and self._cells[i-1][j].visited == False:
            self._cells[i][j].draw_move(self._cells[i-1][j], False)
            if self._solve_r(i-1, j):
                 return True
            else:
                self._cells[i][j].draw_move(self._cells[i-1][j], True)

              #right
        if i < self._num_cols - 1 and self._cells[i][j].has_right_wall == False and self._cells[i+1][j].visited == False:
            self._cells[i][j].draw_move(self._cells[i+1][j], False)
            if self._solve_r(i+1, j):
                 return True
            else:
                self._cells[i][j].draw_move(self._cells[i+1][j], True)                                         

        return False
