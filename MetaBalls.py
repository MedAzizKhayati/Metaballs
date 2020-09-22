import pygame
import math
from pygame import gfxdraw
import random
import numpy
import numba as nb
from _thread import *
import os

pygame.init()
height = 720
width = 1280
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Metaballs")
CORES = os.cpu_count()
balls = []
screen = numpy.zeros((width, height, 3), dtype=numpy.int32)

class metaball:
    def __init__(self):
        self.r = random.randint(30, 50)
        self.coords = [random.randint(30, 1250), random.randint(30, 690)]
        self.vel = [random.randint(-3, 3), random.randint(-3, 3)]
        while self.vel == [0, 0]:
            self.vel = [random.randint(-3, 3), random.randint(-3, 3)]

    def move(self):
        if self.r >= self.coords[0] or self.coords[0] >= 1280 - self.r:
            self.vel[0] *= -1
        if self.r >= self.coords[1] or self.coords[1] >= 720 - self.r:
            self.vel[1] *= -1
        self.coords[0] += self.vel[0]
        self.coords[1] += self.vel[1]

    def draw(self, win):
        draw_circle(win, self.coords[0], self.coords[1], self.r, (255, 0, 100))


def draw_circle(surface, x, y, radius, color):
    gfxdraw.aacircle(surface, x, y, radius, color)
    gfxdraw.filled_circle(surface, x, y, radius, color)


def ball_generation():
    global balls
    num = random.randint(3, 10)
    for i in range(0, num):
        balls.append(metaball())


@nb.njit(parallel=True, fastmath=True)
def pixel():
    global win, screen
    for start in nb.prange(CORES):
        for x in range(start, width, CORES):
            for y in range(height):
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                for c in range(3):
                    print(screen[x, y, c])
                    screen[x, y, c] = 2


def pixel_colors(win):
    for i in balls:
        for j in balls:
            if j != i:
                a = numpy.array(i.coords)
                b = numpy.array(j.coords)
                if numpy.linalg.norm(a - b) < 100:
                    pass
            # for k in range(min(a[0], b[0]), max(a[0], b[0])):
            #     for l in range(min(a[1] - i.r, a[1] + i.r, b[1] - j.r, b[1] + j.r),
            #                    max(a[1] - i.r, a[1] + i.r, b[1] - j.r, b[1] + j.r)):
            #         c = numpy.array([k, l])
            #         if numpy.linalg.norm(a - c) < 100 or numpy.linalg.norm(b - c) < 100:
            #             gfxdraw.pixel(win, k, l, (255, 0, 100))


def main():
    global screen
    run = True
    ball_generation()
    clock = pygame.time.Clock()
    while run:
        clock.tick(144)
        #win.fill((255, 0, 255))
        pixel()
        pygame.surfarray.blit_array(win, screen)
        for i in balls:
            i.move()
            i.draw(win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()


main()
pygame.quit()
