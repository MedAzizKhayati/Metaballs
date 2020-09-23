import pygame
import math
import time
import os
from pygame import gfxdraw
import numpy as np
import random
import numba as nb

pygame.init()
width = 1000
height = 720
CORES = os.cpu_count()
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gravity")
click = False
clicked = False
blobs = []


class blob:
    def __init__(self):
        self.r = random.randint(30, 50)
        self.rgb = [1, 0, 0]
        self.rgb[random.randint(0, 2)] = 1
        self.coords = [random.randint(50, width - 50), random.randint(50, height - 50)]
        self.vel = [random.randint(-6, 6), random.randint(-6, 6)]
        while self.vel == [0, 0]:
            self.vel = [random.randint(-6, 6), random.randint(-6, 6)]

    def move(self):
        if self.r >= self.coords[0] or self.coords[0] >= width - self.r:
            self.vel[0] *= -1
        if self.r >= self.coords[1] or self.coords[1] >= height - self.r:
            self.vel[1] *= -1
        self.coords[0] += self.vel[0]
        self.coords[1] += self.vel[1]


@nb.njit(parallel=True, fastmath=True)
def update_pixels(coords: np.array, radius: np.array, color: np.array, screen: np.array):
    for start in nb.prange(CORES):
        for x in range(start, width, CORES):
            for y in range(height):
                screen[x, y] = 0
                for i, j, k in zip(coords, radius, color):
                    dx = x - i[0]
                    dy = y - i[1]
                    dist = dx * dx + dy * dy + 0.01
                    r = int(j * j / dist * 255)
                    r = (r * k[0] << 16) + (r * k[1] << 8) + r * k[2]
                    screen[x, y] += r
                    if screen[x][y] > 16777215:
                        screen[x][y] = 16777215
    return screen


def custom_blob(mx, my):
    global click, clicked, blobs
    if click and not clicked:
        blobs.append(blob())
        blobs[len(blobs) - 1].coords = [mx, my]
        blobs[len(blobs) - 1].vel = [0, 0]
        clicked = True
    elif click and clicked:
        blobs[len(blobs) - 1].coords = [mx, my]
    elif not click and clicked:
        clicked = False
        blobs.pop(len(blobs) - 1)


def main():
    global click, clicked, blobs
    run = True
    mx, my = 0, 0
    j = 0
    clock = pygame.time.Clock()
    for i in range(5):
        blobs.append(blob())
    screen = np.zeros(shape=(width, height))
    while run:
        dt = clock.tick() / 1000
        j += 1
        win.fill((255, 255, 255))
        coords = []
        r = []
        color = []
        custom_blob(mx, my)
        for i in blobs:
            i.move()
            coords.append(i.coords)
            r.append(i.r)
            color.append(i.rgb)
        coords = np.array(coords)
        r = np.array(r)
        color = np.array(color)
        update_pixels(coords, r, color, screen)
        pygame.surfarray.blit_array(win, screen)
        click = False
        if pygame.mouse.get_pressed()[0]:
            click = True
            mx, my = pygame.mouse.get_pos()
        if j % 20 == 0:
            print(int(1 / dt))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()


if __name__ == "__main__":
    main()
pygame.quit()
