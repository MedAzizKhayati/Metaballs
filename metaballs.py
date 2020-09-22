import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import random
import numpy as np
import numba as nb
import math

pygame.init()
width = 1280
height = 720
win = pygame.display.set_mode((1280, 720), DOUBLEBUF | OPENGL)
pygame.display.set_caption("3D Cube Emulator")


class cube:
    # colors = []
    # for i in range(6):
    #     colors.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    def __init__(self, coords, size):
        self.x = x = coords[0]
        self.y = y = coords[1]
        self.z = z = coords[2]
        size = size // 2
        self.vertices = [[x - size, y - size, z - size],
                         [x - size, y + size, z - size],
                         [x + size, y + size, z - size],
                         [x + size, y - size, z - size],
                         [x - size, y - size, z + size],
                         [x - size, y + size, z + size],
                         [x + size, y + size, z + size],
                         [x + size, y - size, z + size]]
        self.faces = [[0, 1, 2, 3], [3, 2, 6, 7], [7, 6, 5, 4], [4, 5, 1, 0], [1, 5, 6, 2], [4, 0, 3, 7]]
        self.lines = [[0, 1], [0, 3], [0, 4], [1, 2], [1, 5], [2, 6], [2, 3], [3, 7], [4, 7], [4, 5], [5, 6], [6, 7]]
        colors = []
        for i in range(6):
            colors.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        self.face_colors = colors

    def rotateX(self, angle):
        cos = math.cos(angle)
        sin = math.sin(angle)
        for p in self.vertices:
            ry = (p[1] - self.y) * cos - (p[2] - self.z) * sin
            rz = (p[2] - self.z) * cos + (p[1] - self.y) * sin
            p[1] = ry + self.y
            p[2] = rz + self.z

    def rotateY(self, angle):
        cos = math.cos(angle)
        sin = math.sin(angle)
        for p in self.vertices:
            rx = (p[0] - self.x) * cos - (p[2] - self.z) * sin
            rz = (p[2] - self.z) * cos + (p[0] - self.x) * sin
            p[0] = rx + self.x
            p[2] = rz + self.z

    def translate(self, vector):
        self.x += vector[0]
        self.y += vector[1]
        self.z += vector[2]
        for i in self.vertices:
            i[0] += vector[0]
            i[1] += vector[1]
            i[2] += vector[2]

    def draw(self):
        glBegin(GL_LINES)
        for face in self.lines:
            for vertex in face:
                glVertex3fv(self.vertices[vertex])
        glEnd()


def main():
    MyCube = cube([0, 0, 0], 2)
    run = True
    gluPerspective(45, (width / height), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    glRotatef(0, 0, 0, 0)
    while run:
        glRotatef(1, 0, 1, 0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        MyCube.draw()
        pygame.display.flip()
        pygame.time.wait(10)


main()
quit()
