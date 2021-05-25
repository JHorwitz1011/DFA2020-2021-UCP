from tkinter import Frame, Label, CENTER
import random

import logic
import vars.constants as c

def gen():
    return random.randint(0, c.GRID_LEN - 1)

class GameGrid(Frame):
    def __init__(self):
        Frame.__init__(self)

        # splits the Frame into rows and columns.
        self.grid()
        # title puts a title in an existing window (so this is putting 2048 as a title in an open window)
        self.master.title('2048')
        
        # binds a kepress to a specific action not 100% sure how this applies to the dict below tho
        self.master.bind("<Key>", self.key_down)

        # dictionary to store key presses and callback functions 
        self.commands = {c.KEY_UP: logic.up, 
                         c.KEY_DOWN: logic.down,
                         c.KEY_LEFT: logic.left, 
                         c.KEY_RIGHT: logic.right,
                         c.KEY_UP_ALT: logic.up, 
                         c.KEY_DOWN_ALT: logic.down,
                         c.KEY_LEFT_ALT: logic.left, 
                         c.KEY_RIGHT_ALT: logic.right,
                         c.KEY_H: logic.left, 
                         c.KEY_L: logic.right,
                         c.KEY_K: logic.up, 
                         c.KEY_J: logic.down}
   
        self.grid_cells = []
        
        #I think this opens the original grid image, before people start making moves (maybe?)
        self.init_grid()
        
        #intializes the matrix
        self.matrix = logic.new_game(c.GRID_LEN)
        
        # not worrying about that
        self.history_matrixs = []
        
        # referneced later in file
        self.update_grid_cells()

        # starts the window/event handler and launches the application
        self.mainloop()        
        
    def init_grid(self):
      
        # initializes the background frame to predefined color and size
        background = Frame(self, bg =c.BACKGROUND_COLOR_GAME,
                           width=c.SIZE, height=c.SIZE)
        
        # cell grid?
        background.grid()
        
        #Note: Padding is just some blank space that surrounds a widget and separates it visually from its contents.
				#initializes the grids and text boxes for the game (light shaded boxes)
        for i in range(c.GRID_LEN):
            grid_row = []
            for j in range(c.GRID_LEN):
              
                cell = Frame(background, bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                             width=c.SIZE / c.GRID_LEN,
                             height=c.SIZE / c.GRID_LEN)
                cell.grid(row=i, column=j, padx=c.GRID_PADDING,
                          pady=c.GRID_PADDING)
                t = Label(master=cell, text="",
                          bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                          justify=CENTER, font=c.FONT, width=5, height=2)
                t.grid()
                # collects all the elements into a row 
                grid_row.append(t)

            #collects the rows (adds onto the grid cell list) and puts them into columns onto the background
            self.grid_cells.append(grid_row)

    def update_grid_cells(self):
      #configure: not 100% sure, but can be inferred that configure edits properties of a widget in the frame
      # loop through matrix and update visuals of cells if a cell's number is not 0
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                new_number =  self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(new_number), bg=c.BACKGROUND_COLOR_DICT[new_number],
                                                    fg=c.CELL_COLOR_DICT[new_number])
        # forces a redraw of the window
        self.update_idletasks()

    # runs whenever key is pressed
    def key_down(self, event):
        # determines key press
        key = repr(event.char)
        
        # "rewind" feature of the game
        if key == c.KEY_BACK and len(self.history_matrixs) > 1:
            self.matrix = self.history_matrixs.pop()
            self.update_grid_cells()
            print('back on step total step:', len(self.history_matrixs))  
        
        # check if keypress is a valid key in dictionary commands
        elif key in self.commands:
            # takes a valid key press and calls the corresponding callback function in the logic.py file
            self.matrix, done = self.commands[repr(event.char)](self.matrix)
            
            # cleanup if it was successful? eileen handle
            if done:
                self.matrix = logic.add_two(self.matrix)
                # record last move
                self.history_matrixs.append(self.matrix)
                self.update_grid_cells()
                if logic.game_state(self.matrix) == 'win':
                    self.grid_cells[1][1].configure(text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Win!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                if logic.game_state(self.matrix) == 'lose':
                    self.grid_cells[1][1].configure(text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Lose!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)

  	# ??? wth
    def generate_next(self):
        index = (gen(), gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (gen(), gen())
        self.matrix[index[0]][index[1]] = 2

# starts the game
game_grid = GameGrid()
