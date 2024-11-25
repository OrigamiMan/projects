import turtle as t
import math
t.speed(0)
def draw_square(x, y, side):
    for _ in range(4):
        t.forward(side)
        t.left(90)

def draw_crossed_square(x, y, side):
    t.penup()
    t.setpos(x-side/2, y-side/2)
    t.pendown()
    draw_square(x, y, side)
    for _ in range(2):
        t.left(45)
        t.forward(math.sqrt(2)*side)
        t.left(135)
        t.forward(side)
        t.left(90)

Lock = False

def each_click(x, y):
    global Lock
    if Lock:
        return
    Lock = True
    draw_crossed_square(x, y, 50)
    Lock = False

t.onscreenclick(each_click)






t.mainloop()