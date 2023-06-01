"""
Modeling the movement of cosmic bodies
"""

import numpy as np
import matplotlib.pyplot as plt
import pygame
import math


def run_cosmos(width, height, x_10, y_10, x_20, y_20):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Elliptical Motion")
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)

    center_x, center_y = width // 2, height // 2

    running = True
    clock = pygame.time.Clock()
    path_0 = []
    path_1 = []
    ind = 0
    while running:
        draw = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        try:
            x_0 = int(center_x + x_10[ind]*100)
            y_0 = int(center_y + y_10[ind]*100)
            x_1 = int(center_x + x_20[ind]*100)
            y_1 = int(center_y + y_20[ind]*100)
        except IndexError:
            ind = 0
            path_0 = [(center_x + x_10[ind+1]*100, center_y + y_10[ind+1]*100)]
            path_1 = [(center_x + x_20[ind+1]*100, center_y + y_20[ind+1]*100)]
            draw = False

        screen.fill(BLACK)

        pygame.draw.circle(screen, YELLOW, (center_x, center_y), 10)
        pygame.draw.circle(screen, GREEN, (x_0, y_0), 10)
        pygame.draw.circle(screen, RED, (x_1, y_1), 10)

        path_0.append((x_0, y_0))
        path_1.append((x_1, y_1))

        # Draw the path of each circle
        if draw:
            for i in range(len(path_0) - 1):
                pygame.draw.line(screen, GREEN, path_0[i], path_0[i + 1], 1)
            for i in range(len(path_1) - 1):
                pygame.draw.line(screen, RED, path_1[i], path_1[i + 1], 1)

        pygame.display.flip()
        clock.tick(150)
        ind += 1


def calc(tFinal, dt, f0, GM, M, m1, m2, r1, r2):
    t = np.arange(0, tFinal + dt, dt)
    f = np.zeros((len(t), len(f0)))
    f[0] = f0

    for i in range(1, len(t)):
        r13 = (np.sqrt(f[i-1, 0]**2 + f[i-1, 1]**2))**3
        r23 = (np.sqrt(f[i-1, 4]**2 + f[i-1, 5]**2))**3
        dx12 = f[i-1, 4] - f[i-1, 0]
        dy12 = f[i-1, 5] - f[i-1, 1]
        r123 = (np.sqrt(dx12**2 + dy12**2))**3

        f[i, 2] = f[i-1, 2] - dt * (GM / r13 * f[i-1, 0] - GM * m2 / M / r123 * dx12)
        f[i, 3] = f[i-1, 3] - dt * (GM / r13 * f[i-1, 1] - GM * m2 / M / r123 * dy12)
        f[i, 6] = f[i-1, 6] - dt * (GM / r23 * f[i-1, 4] - GM * m1 / M / r123 * dx12)
        f[i, 7] = f[i-1, 7] - dt * (GM / r23 * f[i-1, 5] - GM * m1 / M / r123 * dy12)

        f[i, 0] = f[i-1, 0] + dt * f[i, 2]
        f[i, 1] = f[i-1, 1] + dt * f[i, 3]
        f[i, 4] = f[i-1, 4] + dt * f[i, 6]
        f[i, 5] = f[i-1, 5] + dt * f[i, 7]
    return t, f

if __name__ == '__main__':
    GM = 4 * np.pi**2
    M = 1.99e30
    m1 = 5.9737e24
    m2 = m1 * 0.107
    r1 = 1
    r2 = 1.524
    x10 = r1
    y10 = 0
    vx10 = 0
    vy10 = np.sqrt(GM / r1)
    x20 = r2
    y20 = 0
    vx20 = 0
    vy20 = np.sqrt(GM / r2)
    dt = 0.005
    tFinal = 10

    f0 = [x10, y10, vx10, vy10, x20, y20, vx20, vy20]

    t, f = calc(tFinal, dt, f0, GM, M, m1, m2, r1, r2)

    x_10 = f[:, 0]
    y_10 = f[:, 1]
    vx_10 = f[:, 2]
    vy_10 = f[:, 3]
    print(vx10, vy10)
    x_20 = f[:, 4]
    y_20 = f[:, 5]
    vx_20 = f[:, 6]
    vy_20 = f[:, 7]

    
    # plt.figure(1)
    # plt.plot(t, f[:, 0], t, f[:, 4], t, f[:, 1], t, f[:, 5])
    # plt.figure(2)
    # plt.plot(t, f[:, 2], t, f[:, 3], t, f[:, 6], t, f[:, 7])
    # plt.figure(3)
    # plt.plot(f[:, 0], f[:, 1], f[:, 4], f[:, 5])

    # plt.show()
    run_cosmos(800, 800, x_10, y_10, x_20, y_20)
