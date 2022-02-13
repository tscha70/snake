import sys
import numpy as np
import pygame
import winsound

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PINK = (233, 33, 227)
GREEN = (0, 102, 0)


def playGameoverSound():
    tone_len = 100
    for tone in range(250, 100, -50):
        tone_len *= 2
        winsound.Beep(tone, tone_len)


def textObject(text, myfont):
    text_flaeche = myfont.render(text, True, (255, 255, 255))
    return text_flaeche, text_flaeche.get_rect()


def zeichner():
    screen.fill(GREEN)

    # draw apples
    for a in apfelCoords:
        coords = [a[0] * partikel, a[1] * partikel]
        points = [[coords[0], coords[1] + partikel / 4], [coords[0] + partikel / 2, coords[1] + partikel],
                  [coords[0] + partikel - 1, coords[1] + partikel / 4]]
        pygame.draw.polygon(screen, RED, points, 0)
        pl = [coords[0] + partikel / 4, coords[1] + partikel / 4]
        pr = [coords[0] + partikel - partikel / 4, coords[1] + partikel / 4]
        pygame.draw.circle(screen, RED, pl, partikel / 4)
        pygame.draw.circle(screen, RED, pr, partikel / 4)

        # pygame.draw.rect(screen, RED, (coords[0], coords[1], partikel, partikel), 0)
    kopf = True

    # draw snake
    for p in schlange:
        coords = [p[0] * partikel, p[1] * partikel]
        if kopf:
            pygame.draw.rect(screen, YELLOW, (coords[0], coords[1], partikel, partikel), 0)
            kopf = False
        else:
            pygame.draw.rect(screen, PINK, (coords[0], coords[1], partikel, partikel), 0)


def apfelCoordGen():
    while True:
        coord = [np.random.randint(0, maxHorizontal / partikel), np.random.randint(0, maxVertical / partikel)]
        change = False
        for p in schlange:
            if coord == p:
                change = True
        for p in apfelCoords:
            if coord == p:
                change = True
        if not change:
            return coord


# initialize the game
partikel = 25
schlange = [[13, 13], [13, 14]]
apfelCoords = []
richtung = 0
maxHorizontal = 700
maxVertical = 500
go = True
anhang = None
apfelInd = -1
ende = False
score = 0

pygame.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont('arialblack', 25)
screen = pygame.display.set_mode([maxHorizontal, maxVertical])
pygame.display.set_caption('Snake - use WASD-keys or arrow-keys to control the snake')

while True:
    # get the directions from input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_KP8 or event.key == pygame.K_w) and richtung != 2:
                richtung = 0
            if (event.key == pygame.K_RIGHT or event.key == pygame.K_KP6 or event.key == pygame.K_d) and richtung != 3:
                richtung = 1
            if (event.key == pygame.K_DOWN or event.key == pygame.K_KP2 or event.key == pygame.K_s) and richtung != 0:
                richtung = 2
            if (event.key == pygame.K_LEFT or event.key == pygame.K_KP4 or event.key == pygame.K_a) and richtung != 1:
                richtung = 3

    if anhang is not None:
        schlange.append(anhang.copy())
        anhang = None
        apfelCoords.pop(apfelInd)

    zahl = len(schlange) - 1
    for i in range(1, len(schlange)):
        schlange[zahl] = schlange[zahl - 1].copy()
        zahl -= 1

    # Moving Snake
    if richtung == 0:
        schlange[0][1] -= 1
    if richtung == 1:
        schlange[0][0] += 1
    if richtung == 2:
        schlange[0][1] += 1
    if richtung == 3:
        schlange[0][0] -= 1

    # Collision Detection
    for x in range(1, len(schlange)):
        if schlange[0] == schlange[x]:
            ende = True

    # Horizontal boundaries
    if schlange[0][0] < 0 or schlange[0][0] >= maxHorizontal / partikel:
        ende = True

    # Vertical boundaries
    if schlange[0][1] < 0 or schlange[0][1] >= maxVertical / partikel:
        ende = True

    # Eat apple
    for x in range(0, len(apfelCoords)):
        if apfelCoords[x] == schlange[0]:
            anhang = schlange[-1].copy()
            apfelInd = x
            score += 10
            winsound.Beep(1000, 50)

    # Generate new apples
    zufall = np.random.randint(0, 100)
    if zufall < 50 and len(apfelCoords) < 20 or len(apfelCoords) == 0:
        apfelCoords.append(apfelCoordGen())

    if not ende:
        zeichner()
        text_grund, text_kasten = textObject("Babsi's Valentine Score: " + str(score), font)
        text_kasten.center = (maxHorizontal / 2, 40)
        screen.blit(text_grund, text_kasten)
        pygame.display.update()
    else:
        gameover = True
        playGameoverSound()
        while gameover:
            text_grund, text_kasten = textObject("Game over!", font)
            text_kasten.center = (maxHorizontal / 2, 80)
            screen.blit(text_grund, text_kasten)
            text_grund, text_kasten = textObject("'n' = new game, x = exit", font)
            text_kasten.center = (maxHorizontal / 2, 120)
            screen.blit(text_grund, text_kasten)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        schlange = [[13, 13], [13, 14]]
                        apfelCoords = []
                        richtung = 0
                        apfelCoords.append(apfelCoordGen())
                        ende = False
                        gameover = False
                        score = 0
                    if event.key == pygame.K_x:
                        playing = False
                        sys.exit()
    clock.tick(6)
