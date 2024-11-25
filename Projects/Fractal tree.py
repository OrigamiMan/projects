import turtle as tu
pen = tu.Turtle()
pen.left(90)
pen.speed(0)
pen.backward(250)
pen.clear()
pen.hideturtle()


def draw(i):
    if (i<3):
        return
    else:
        pen.forward(i)
        pen.left(35)
        draw(3*i/4)
        pen.right(50)
        draw(3*i/4)
        pen.left(15)
        pen.backward(i)


draw(150)