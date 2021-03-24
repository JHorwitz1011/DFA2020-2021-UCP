from tkinter import *
from tkinter import ttk
from constants import *

##CONSTANTS##


class GameBoard(Canvas):

    def __init__(self, parent,**kwargs):
        Canvas.__init__(self, parent,**kwargs)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth() 
        self.pieces = []
        self.bind("<Configure>", self.on_resize)


        # config settings
        self['bg'] = BACKGROUND_COLOR_GAME #background color
        self['bd'] = 0 #border width pixels


       # c = self.create_rectangle(, 10, 100, 100,fill=BACKGROUND_COLOR_CELL_EMPTY,width=GRID_PADDING/2)
        #c['bg'] = BACKGROUND_COLOR_CELL_EMPTY
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                pad_offset = GRID_PADDING
                x0 = i*SQUARE_SIDE + pad_offset*(1+i)
                y0 = j*SQUARE_SIDE + pad_offset*(j+1)
                x1 = (i + 1)*SQUARE_SIDE + pad_offset*(1+i)
                y1 = (j + 1)*SQUARE_SIDE + pad_offset*(j+1)
                c = self.create_rectangle(x0, y0, x1, y1,
                                          fill=BACKGROUND_COLOR_CELL_EMPTY,width=0)

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas 
        #self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,hscale)
        print(self.height, self.width)

#lets us import the class without worrying about the script accidentally running
if __name__ == '__main__':
    root = Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    side = GRID_LEN *( SQUARE_SIDE + GRID_PADDING ) + GRID_PADDING
    canvas = GameBoard(root,width=side,height=side)
    canvas.pack(fill=BOTH, expand=YES)

    canvas.addtag_all('all')
    root.mainloop()
    print(canvas.height, canvas.width)