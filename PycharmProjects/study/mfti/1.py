import turtle
import math

def drawFigure(ttl, degree):
    angle = 360/degree
    edge = 10*degree
    if degree < 3:
        exit(33)
    for i in range(degree):
        ttl.forward(edge)
        ttl.left(angle)




leo = turtle.Turtle()
leo.shape('turtle')


x = 3
while x < 13:
    r = 10*(x-2)/float(math.sin(180/x))
    print(math.sin(180 - 180/x))
    #print(r)
    leo.penup()
    leo.goto(r, 0)
    leo.pendown()
    drawFigure(leo, x)
    x+=1



