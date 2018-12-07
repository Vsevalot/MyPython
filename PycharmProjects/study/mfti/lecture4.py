#!/usr/bin/python3
# -*- coding: utf-8 -*-

import graphics as gr
import math

SIZE_X = 800
SIZE_Y = 800

class Pendulum(gr.Circle):
    def __init__(self, centre, radius, color):
        super().__init__(centre, radius)
        self.setFill(color)

        self.radius = radius
        self.x = centre.x
        self.y = centre.y
        self.velocity = {'x': 0, 'y': 0}


if __name__ == "__main__":
    window = gr.GraphWin("Model", SIZE_X, SIZE_Y)

    #  initial coordinates of the ball
    pendulum = Pendulum(gr.Point(200, 500), 15, "red")
    pendulum.draw(window)

    clamping = Pendulum(gr.Point(400, 5), 5, "black")
    clamping.draw(window)

    vector = gr.Point(pendulum.p1.x + pendulum.radius - 400, pendulum.p1.y + pendulum.radius - 795)
    module = math.sqrt(vector.x ** 2 + vector.y ** 2)

    while True:
        g = 1
        vector = gr.Point(-(pendulum.p1.x + pendulum.radius - 400), -(pendulum.p1.y + pendulum.radius - 795))
        module = math.sqrt(vector.x ** 2 + vector.y ** 2)
        print(pendulum.p1.x, pendulum.p1.y, module)
        ax = g * vector.x / module
        ay = -g + g * vector.y / module
        pendulum.velocity['x'] += ax
        pendulum.velocity['y'] -= ay
        pendulum.move(pendulum.velocity['x'], pendulum.velocity['y'])

        gr.time.sleep(0.05)








