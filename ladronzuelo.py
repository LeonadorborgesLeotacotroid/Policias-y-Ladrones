import pygame
import numpy as np
import time
import random
from pygame.locals import *

pygame.init()
pygame.display.set_caption('Policías y Ladrones')

width, height = 750, 750
screen = pygame.display.set_mode((height, width))
defaultFont = pygame.font.Font(None, 30)
pauseText = defaultFont.render("PAUSADO", True, (203, 50, 52), 0)

bg = 25, 25, 25
screen.fill(bg)

nxC, nyC = 25, 25

dimCW = width / nxC
dimCH = height / nyC


gameState = np.zeros((nxC, nyC))


gameState[5, 5] = 1
gameState[10, 10] = 2
gameState[15, 15] = 2

pauseExec = False
update_interval_paused = 0.1
update_interval_playing = 0.5

def get_neighbors(x, y):
    return [((x - 1) % nxC, (y - 1) % nyC), ((x) % nxC, (y - 1) % nyC), ((x + 1) % nxC, (y - 1) % nyC), 
            ((x - 1) % nxC, (y) % nyC), ((x + 1) % nxC, (y) % nyC), 
            ((x - 1) % nxC, (y + 1) % nyC), ((x) % nxC, (y + 1) % nyC), ((x + 1) % nxC, (y + 1) % nyC)]

while True:
    newGameState = np.copy(gameState)
    screen.fill(bg)

    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.KEYDOWN:
            pauseExec = not pauseExec

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            if mouseClick[0]:  # click izquierdo: Policia
                newGameState[celX, celY] = 1
            elif mouseClick[2]:  # Click derechi: Ladron
                newGameState[celX, celY] = 2

    update_interval = update_interval_paused if pauseExec else update_interval_playing
    time.sleep(update_interval)

    for y in range(nxC):
        for x in range(nyC):
            if not pauseExec:
                neighbors = get_neighbors(x, y)
                thief_neighbors = [n for n in neighbors if gameState[n[0], n[1]] == 2]
                police_neighbors = [n for n in neighbors if gameState[n[0], n[1]] == 1]

                if gameState[x, y] == 2:  # TLogica del ladron
                    if len(police_neighbors) >= 3:
                        newGameState[x, y] = 1  # Spawneo de policia
                    else:
                        empty_neighbors = [n for n in neighbors if gameState[n[0], n[1]] == 0]
                        if empty_neighbors:
                            new_pos = random.choice(empty_neighbors)
                            newGameState[x, y] = 0
                            newGameState[new_pos[0], new_pos[1]] = 2

                elif gameState[x, y] == 1:  # Logica de policia
                    if len(thief_neighbors) >= 2:
                        newGameState[x, y] = 0  # Muerte de policia
                    else:
                        if thief_neighbors:
                            new_pos = random.choice(thief_neighbors)
                            newGameState[x, y] = 0
                            newGameState[new_pos[0], new_pos[1]] = 1
                        else:
                            empty_neighbors = [n for n in neighbors if gameState[n[0], n[1]] == 0]
                            if empty_neighbors:
                                new_pos = random.choice(empty_neighbors)
                                newGameState[x, y] = 0
                                newGameState[new_pos[0], new_pos[1]] = 1

            poly = [(x * dimCW, y * dimCH),
                    ((x + 1) * dimCW, y * dimCH),
                    ((x + 1) * dimCW, (y + 1) * dimCH),
                    (x * dimCW, (y + 1) * dimCH)]
            
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            elif newGameState[x, y] == 1:
                pygame.draw.polygon(screen, (0, 0, 255), poly, 0)  # Policia azul
            elif newGameState[x, y] == 2:
                pygame.draw.polygon(screen, (255, 0, 0), poly, 0)  # Ladron Rojo

    if pauseExec:
        screen.blit(pauseText, (0, 730))

    gameState = np.copy(newGameState)
    pygame.display.flip()

