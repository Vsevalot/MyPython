import pygame
import random

WIDTH = 800
HIGH = 600

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

game_display = pygame.display.set_mode((WIDTH, HIGH))
pygame.display.set_caption("Bubble world")
clock = pygame.time.Clock()


class Bubble:
    def __init__ (self, color):
        self.x = random.randrange(0,WIDTH)
        self.y = random.randrange(0,HIGH)
        self.radius = random.randrange(10,20)
        self.color = color

    def move(self):
        self.x += random.randrange(-1,2)
        self.y += random.randrange(-1,2)

        if self.x > WIDTH: self.x = WIDTH
        elif self.x < 0: self.x = 0

        if self.y > HIGH: self.y = HIGH
        elif self.y < 0: self.y = 0


def draw_environment(bubble_list):
    game_display.fill(WHITE)
    for bubble in bubble_list:
        pygame.draw.circle(game_display, bubble.color, [bubble.x, bubble.y], bubble.radius)
        bubble.move()
    pygame.display.update()


def random_color():
    return (random.randrange(0,256), random.randrange(0,256), random.randrange(0,256))


def main(blob_number):
    blobs = [Bubble(random_color()) for i in range(blob_number)]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        draw_environment(blobs)
        clock.tick(60)


if __name__=="__main__":
    main(40)