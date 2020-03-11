import tkinter as tk
from enum import Enum
import time
from queue import Queue
from random import randrange

GAMEBOARD_BG = 'gray'
GAMEBOARD_WIDTH = 700
GAMEBOARD_HIEGHT = 500
DOT_SIZE = 10

X_BORDER = GAMEBOARD_WIDTH/DOT_SIZE
Y_BORDER = GAMEBOARD_HIEGHT/DOT_SIZE

SPEED = 0.05
DEFAULT_APPLES = 2

def getOvalLocation(x , y):
    x = 10 + x * DOT_SIZE
    y = 10 + y * DOT_SIZE
    return (x - 5, y - 5, x + 5, y + 5)

def get_next_step(head, direction):
    if direction == Direction.UP:
        head[1] -= 1
    elif direction == Direction.DOWN:
        head[1] += 1
    elif direction == Direction.RIGHT:
        head[0] += 1
    elif direction == Direction.LEFT:
        head[0] -= 1

def in_border(x ,y):

    if x < 0 or y < 0 or x >= X_BORDER or y >= Y_BORDER:
        return False
    return True

def get_rand_location():
    return randrange(0, X_BORDER), randrange(0, Y_BORDER)

            
class Direction(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4
        
class Snake():
    
    def __init__(self, start_location):
        self.start_location = start_location

    def get_body(self):
        pass

    def add_body(self):
        pass

    

class Application(tk.Frame):

    direction = Direction.RIGHT
    default_location = [35, 25]
    head = default_location[:]
    snake = Queue()
    default_length = 5

    apples = {}
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.start = tk.Button(self)
        self.start["text"] = "Start\n(click me)"
        self.start["command"] = self.move
        self.start.pack(side="top")

        self.gameboard = tk.Canvas(self, width=700, height=500, bg=GAMEBOARD_BG, bd=1)
        self.make_default_snake()
        self.make_default_apples()

        self.gameboard.pack(side='bottom')

    def paintOval(self, x , y, color = 'black'):
        l = getOvalLocation(x,y)
        return self.gameboard.create_oval(*l, fill=color)
        
    def make_default_snake(self):

        self.default_location[0] -= self.default_length - 1 

        locations = ((self.default_location[0] + i, self.default_location[1])
                     for i in range(self.default_length))

        for x, y in locations:
            self.snake.put(self.paintOval(x,y))

    def paint_apple(self):

        apple_loc = get_rand_location()
        self.apples[apple_loc] = self.paintOval(*apple_loc, color='purple')

    def make_default_apples(self):
        for i in range(DEFAULT_APPLES):
            self.paint_apple()

    def change_dir(self, event):
        try:
            print(type(event.keysym.upper()))
            self.direction = Direction[event.keysym.upper()]

        except Exception as e:
            print(e)
            print('wrong key')
        print(self.direction)
        
        return



    def move(self):
            self.master.bind('<Key>', self.change_dir)
            while True:
                get_next_step(self.head, self.direction)
                if in_border(*self.head):
                    if tuple(self.head) in self.apples.keys():
                        self.gameboard.delete(self.apples[tuple(self.head)])
                        self.snake.put(self.paintOval(*self.head, color='green'))
                        self.paint_apple()
                    else:
                        self.snake.put(self.paintOval(*self.head))
                        self.gameboard.delete(self.snake.get())
                    self.gameboard.update()
                    time.sleep(SPEED)
                else:
                    break

root = tk.Tk()
root.geometry('800x600')
app = Application(master=root)
app.mainloop()
