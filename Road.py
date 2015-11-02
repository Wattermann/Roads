###############
# Road.py
# Ian Watterson October 30, 2015
# Base class for displaying a road object.
# At the moment it is just lines
###############

import pygame
import math
import Bezier
import VectMath

class Road:
    startPos = []
    control00 = []
    control01 = []
    endPos = []
    beziers = []
    leftbez = []
    rightbez = []
    vector = []
    lanes = 2

    def __init__(self,start,mod0,mod1,end):
        self.startPos = start
        self.control00 = mod0
        self.control01 = mod1
        self.endPos = end
        self.beziers = Bezier.GetAllBezierPoints([self.startPos,self.control00,self.control01,self.endPos])
        [self.leftbez,self.rightbez] = self.calculateLaneBeziers(self.startPos,self.control00,self.control01,self.endPos)

    # Drawing function
    def draw(self,screen):
        pygame.draw.aalines(screen, (216,166,33), False, self.beziers)
        pygame.draw.aalines(screen, (0,0,0), False, self.leftbez)
        pygame.draw.aalines(screen, (0,0,0), False, self.rightbez)
        #self.debugDraw(screen)

    # Calculates the points that create vectors of 10 units extending perpendicularly from the endpoints
    def calculateEndPerpendiculars(self,start,control0,control1,end):
        unitC00 = VectMath.unitvect([control0[0]-start[0],control0[1]-start[1]])
        #unitControl00 = [self.startPos[0]+(10*unitC00[0]),self.startPos[1]+(10*unitC00[1])]
        perpUnitStartLeft = [start[0]+(10*unitC00[1]),start[1]-(10*unitC00[0])]
        perpUnitStartRright = [start[0]-(10*unitC00[1]),start[1]+(10*unitC00[0])]

        unitC01 = VectMath.unitvect([control1[0]-end[0],control1[1]-end[1]])
        #unitControl01 = [self.endPos[0]+(10*unitC01[0]),self.endPos[1]+(10*unitC01[1])]
        perpUnitEndLeft = [end[0]-(10*unitC01[1]),end[1]+(10*unitC01[0])]
        perpUnitEndRight = [end[0]+(10*unitC01[1]),end[1]-(10*unitC01[0])]


        return [perpUnitStartLeft,perpUnitStartRright,perpUnitEndLeft,perpUnitEndRight]

    # Calculates the points that create unit vectors perpendicular from the endpoints
    def calculateUnitPerpendiculars(self,start,control0,control1,end):
        unitC00 = VectMath.unitvect([control0[0]-start[0],control0[1]-start[1]])
        perpUnitStartLeft = [0+unitC00[1],0-unitC00[0]]
        perpUnitStartRright = [0-unitC00[1],0+unitC00[0]]

        unitC01 = VectMath.unitvect([control1[0]-end[0],control1[1]-end[1]])
        perpUnitEndLeft = [0-unitC01[1],0+unitC01[0]]
        perpUnitEndRight = [0+unitC01[1],0-unitC01[0]]

        return [perpUnitStartLeft,perpUnitStartRright,perpUnitEndLeft,perpUnitEndRight]

    # Calculates the bezier curves for the edges of the road.
    def calculateLaneBeziers(self,start,control0,control1,end):
        perpendiculars = self.calculateEndPerpendiculars(start,control0,control1,end)
        SLP = [perpendiculars[0][0],perpendiculars[0][1]]
        SRP = [perpendiculars[1][0],perpendiculars[1][1]]
        ELP = [perpendiculars[2][0],perpendiculars[2][1]]
        ERP = [perpendiculars[3][0],perpendiculars[3][1]]

        unitPerps = self.calculateUnitPerpendiculars(start,control0,control1,end)
        uSLP = [unitPerps[0][0],unitPerps[0][1]]
        uSRP = [unitPerps[1][0],unitPerps[1][1]]
        uELP = [unitPerps[2][0],unitPerps[2][1]]
        uERP = [unitPerps[3][0],unitPerps[3][1]]
        SLPControl = [control0[0]+uSLP[0]*10+uELP[0]*10,control0[1]+uSLP[1]*10+uELP[1]*10]
        SRPControl = [control0[0]+uSRP[0]*10+uERP[0]*10,control0[1]+uSRP[1]*10+uERP[1]*10]
        ELPControl = [control1[0]+uSLP[0]*10+uELP[0]*10,control1[1]+uSLP[1]*10+uELP[1]*10]
        ERPControl = [control1[0]+uSRP[0]*10+uERP[0]*10,control1[1]+uSRP[1]*10+uERP[1]*10]

        leftbez = Bezier.GetAllBezierPoints([SLP,SLPControl,ELPControl,ELP])
        rightbez = Bezier.GetAllBezierPoints([SRP,SRPControl,ERPControl,ERP])

        return [leftbez,rightbez]

    # Shows the perpendicular vectors and control vectors for the bezier curves
    def debugDraw(self,screen):
        # Perpendiculars at the ends
        perpendiculars = self.calculateEndPerpendiculars(self.startPos,self.control00,self.control01,self.endPos)
        SLP = [perpendiculars[0][0],perpendiculars[0][1]]
        SRP = [perpendiculars[1][0],perpendiculars[1][1]]
        ELP = [perpendiculars[2][0],perpendiculars[2][1]]
        ERP = [perpendiculars[3][0],perpendiculars[3][1]]

        pygame.draw.aaline(screen,(255,0,0),self.startPos,SLP)
        pygame.draw.aaline(screen,(0,255,0),self.startPos,SRP)
        pygame.draw.aaline(screen,(255,0,0),self.endPos,ELP)
        pygame.draw.aaline(screen,(0,255,0),self.endPos,ERP)
        pygame.draw.aaline(screen,(0,0,255),self.startPos,self.control00)
        pygame.draw.aaline(screen,(255,0,0),self.endPos,self.control01)

        # Unit Perpendiculars for calculating beziers for lanes.
        unitPerps = self.calculateUnitPerpendiculars(self.startPos,self.control00,self.control01,self.endPos)
        uSLP = [unitPerps[0][0],unitPerps[0][1]]
        uSRP = [unitPerps[1][0],unitPerps[1][1]]
        uELP = [unitPerps[2][0],unitPerps[2][1]]
        uERP = [unitPerps[3][0],unitPerps[3][1]]
        SLPControl = [self.control00[0]+uSLP[0]*10+uELP[0]*10,self.control00[1]+uSLP[1]*10+uELP[1]*10]
        SRPControl = [self.control00[0]+uSRP[0]*10+uERP[0]*10,self.control00[1]+uSRP[1]*10+uERP[1]*10]
        ELPControl = [self.control01[0]+uSLP[0]*10+uELP[0]*10,self.control01[1]+uSLP[1]*10+uELP[1]*10]
        ERPControl = [self.control01[0]+uSRP[0]*10+uERP[0]*10,self.control01[1]+uSRP[1]*10+uERP[1]*10]

        # Bezier Control Lines
        pygame.draw.aaline(screen,(0,0,255),SLP,SLPControl)
        pygame.draw.aaline(screen,(0,0,255),SRP,SRPControl)
        pygame.draw.aaline(screen,(255,0,0),ELP,ELPControl)
        pygame.draw.aaline(screen,(255,0,0),ERP,ERPControl)