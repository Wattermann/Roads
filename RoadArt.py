###############
# RoadArt.py
# Ian Watterson October 28, 2015
# Simple pygame to draw roads. Later will expand upon this.
###############

import sys
import pygame
import Bezier
import math
import VectMath
import RealtimeDraw as rd
from Road import Road

screen = pygame.display.set_mode((800, 600))
screen.fill((255, 255, 255))
pygame.display.update()

# Drawing the current road being built
def realtimeDraw(screen,mousepos,buildPos):
    # Initial Click
    if len(buildPos) == 1:
        # Middle Line
        pygame.draw.aaline(screen,(216,166,33),buildPos[0],mousepos)
        # Edges
        if not (mousepos[0] == buildPos[0][0] and mousepos[1] == buildPos[0][1]):
            # These are the points that are perpendicularly 10 units away from the ends
            perpendiculars = rd.calculatePerpendiculars(buildPos[0],mousepos)
            SLP = [perpendiculars[0][0],perpendiculars[0][1]]
            SRP = [perpendiculars[1][0],perpendiculars[1][1]]
            ELP = [perpendiculars[2][0],perpendiculars[2][1]]
            ERP = [perpendiculars[3][0],perpendiculars[3][1]]
            pygame.draw.aaline(screen,(0,0,0),SLP,ELP)
            pygame.draw.aaline(screen,(0,0,0),SRP,ERP)
    # Realtime Curves
    elif len(buildPos) == 2:
        controlPoint01 = [mousepos[0]+(buildPos[1][0]-mousepos[0]),mousepos[1]+(buildPos[1][1]-mousepos[1])]
        pygame.draw.aaline(screen,(0,0,255),buildPos[0],buildPos[1])
        pygame.draw.aaline(screen,(255,0,0),mousepos,controlPoint01)
        Bezier.DrawBezier([buildPos[0],buildPos[1],controlPoint01,mousepos],screen,(216,166,33))
        if not (mousepos[0] == buildPos[1][0] and mousepos[1] == buildPos[1][1]):
            [leftbez,rightbez] = rd.calculateLaneBeziers(buildPos[0],buildPos[1],controlPoint01,mousepos)
            pygame.draw.aalines(screen, (0,0,0), False, leftbez)
            pygame.draw.aalines(screen, (0,0,0), False, rightbez)
            #rd.debugDraw(screen,buildPos[0],buildPos[1],controlPoint01,mousepos)

# Redrawing every frame
def Redraw(roadList,building,buildPos,mousepos):
    # Background Color
    screen.fill((255, 255, 255))
    # Draw every road. Optimize?
    for road in roadList:
        road.draw(screen)
    # Current road being built
    if building:
        realtimeDraw(screen,mousepos,buildPos)

    pygame.display.update()

###############
# Main
def main():
    clock = pygame.time.Clock()
    roadList = []

    building = False
    buildClick = 0
    mousepos = pygame.mouse.get_pos()
    # Clicked positions so far
    buildPos = []

    while 1:
        # Even Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Exiting")
                sys.exit()

            elif event.type == pygame.MOUSEMOTION:
                mousepos = pygame.mouse.get_pos()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    buildClick = 0
                    building = False
                    #Python3 #buildPos.clear()
                    del buildPos[:]
                    #print("end build")

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if buildClick == 0:
                    building = not building
                    #print("start build")
                #else:
                    #print("start click ",buildClick+1)

            elif event.type == pygame.MOUSEBUTTONUP:
                if building:
                    buildClick+=1
                    buildPos.append(mousepos)
                if buildClick == 3:
                    controlPoint01 = [buildPos[2][0]+(buildPos[1][0]-buildPos[2][0]),buildPos[2][1]+(buildPos[1][1]-buildPos[2][1])]
                    roadList.append(Road(buildPos[0],buildPos[1],controlPoint01,buildPos[2]))
                    buildClick = 1
                    lastClick = buildPos[2]
                    #Python3 #buildPos.clear()
                    del buildPos[:]
                    buildPos.append(lastClick)
                    #print("end build")

        Redraw(roadList,building,buildPos,mousepos)

        clock.tick(30)

###############
# Call main
main()