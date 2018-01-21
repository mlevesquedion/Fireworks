import math
import pygame
import random
import sys
from pygame.locals import *

BLACK = (0, 0, 0)
RED = (240, 40, 40)
GREEN = (40, 240, 40)
BLUE = (40, 40, 240)
YELLOW = (240, 240, 40)
CYAN = (40, 240, 240)
MAGENTA = (240, 40, 240)
COLORS = (RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA)

WIDTH = 1920
HEIGHT = 1080
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), FULLSCREEN)
MAXFIREWORKS = 50
AVGFIREWORKSPERSECOND = 100

CLOCK = pygame.time.Clock()
FPS = 60

GRAVFORCE = -9.81 / FPS

class FireworkParticle:

    PARTICLELAG = 5
    MINPARTICLESPD = 1
    MAXPARTICLESPD = 5
    FADESPD = 5

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.angle = math.radians(random.randint(0, 360))
        self.speed = random.randint(self.MINPARTICLESPD, self.MAXPARTICLESPD)
        self.x_speed = math.cos(self.angle) * self.speed
        self.y_speed = math.sin(self.angle) * self.speed
        self.points = [(self.x, self.y)]
        self.color = color

    def evolve(self):
        self.x += self.x_speed
        self.y += self.y_speed
        self.y_speed -= GRAVFORCE
        self.points.append([self.x, self.y])
        if len(self.points) > self.PARTICLELAG:
            self.points.pop(0)
        self.color = [c - self.FADESPD if c > self.FADESPD else 0 for c in self.color]

    def draw(self):
        pygame.draw.aalines(SCREEN, self.color, False, self.points, True)


class Firework:

    MINPARTICLES = 20
    MAXPARTICLES = 50

    def __init__(self):
        self.particles = []
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        color = random.choice(COLORS)
        for _ in range(random.randint(self.MINPARTICLES, self.MAXPARTICLES + 1)):
            self.particles.append(FireworkParticle(x, y, color))

    def evolve(self):
        for particle in self.particles:
            particle.evolve()

    def draw(self):
        for particle in self.particles:
            particle.draw()

def main():

    while 1:

        SCREEN.fill(BLACK)

        if random.random() > 1 - (AVGFIREWORKSPERSECOND / FPS):
            FIREWORKS.append(Firework())
            if len(FIREWORKS) > MAXFIREWORKS:
                FIREWORKS.pop(0)

        for firework in FIREWORKS:
            firework.evolve()
            firework.draw()

        pygame.display.update()

        CLOCK.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


if __name__ == '__main__':
    FIREWORKS = [Firework()]
    main()
