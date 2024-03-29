from tkinter import *
from constants import *
from PIL import ImageTk, Image
from threading import Thread
import time
class GameBoard(Canvas):

    def __init__(self, parent, **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth() 
        self.pieces = []
        self.bind("<Configure>", self.on_resize)
        #self.bind("<<Test>>",self.test)

        # config settings
        self['bg'] = BACKGROUND_COLOR_GAME #background color
        self['bd'] = 0 #border width pixels


       # c = self.create_rectangle(, 10, 100, 100,fill=BACKGROUND_COLOR_CELL_EMPTY,width=GRID_PADDING/2)
        #c['bg'] = BACKGROUND_COLOR_CELL_EMPTY
        self.draw_background()

        l = Label(self, bg="green",fg="black",text="2",font=("Calibri",15))
        a = self.create_window(10,10,width=100,height=100,window=l,anchor='nw')
        self.pieces.append(a)
        self.update_pieces()
        #self.pieces.append(self.create_rectangle(30, 10, 120, 80, outline="#fb0", fill="#fb0"))

        #self.pieces[0].label

        #self.pieces.append(ImageTk.PhotoImage(Image.open("test.png")))
        #self.create_image(0,0,anchor=NW,image=self.pieces[0])
        #self.tag_lower()
    def test(self):
        print("threading, works!")

    def draw_background(self):
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                pad_offset = GRID_PADDING
                x0 = i*SQUARE_SIDE + pad_offset*(1+i)
                y0 = j*SQUARE_SIDE + pad_offset*(j+1)
                x1 = (i + 1)*SQUARE_SIDE + pad_offset*(1+i)
                y1 = (j + 1)*SQUARE_SIDE + pad_offset*(j+1)
                c = self.create_rectangle(x0, y0, x1, y1,
                                          fill=BACKGROUND_COLOR_CELL_EMPTY,width=0)
    def update_pieces(self):
        print(self.pieces[0].x)
        self.move(self.pieces[0], 0.1, 0.1)
        self.after(10, self.update_pieces)
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
        #root.event_generate("<<Test>>")


if __name__ == '__main__':
    root = Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    #root.resizable(height=False,width=False)
    #root.bind("<<Test>>",threadingtest)
    side = GRID_LEN *( SQUARE_SIDE + GRID_PADDING ) + GRID_PADDING
    canvas = GameBoard(root,width=side,height=side)
    canvas.pack(fill=BOTH, expand=YES)
    canvas.addtag_all('all')
    #label_frame = Frame(root,width=700,height=20,bg="white")
    #label_frame.pack() # Stops child widgets of label_frame from resizing it
   # label_frame.pack()
    #widget = Frame(root, width=SQUARE_SIDE, height=SQUARE_SIDE,bg='red',borderwidth=4)
    #widget.pack()
    #text = Label(widget, text ="test",fg='blue')
    #text.pack()
    #looping(root)
    root.mainloop()
#    loop_thread = Thread(target=looping,args=(root,))
 #   loop_thread.start()
  #  for x in range(10):
   #     time.sleep(1)
        #print('testing thread')
   # loop_thread.join()
    