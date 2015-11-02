###############
# RealtimeDraw.py
# Ian Watterson November 1, 2015
# Didn't want to do static methods for the realtime drawing of lanes in Road.py
###############

import VectMath
import Bezier
import pygame

# Calculates the perpendicular vectors for the endpoints when the road is straight.
def calculatePerpendiculars(start,end):
    unit = VectMath.unitvect([end[0]-start[0],end[1]-start[1]])
    perpUnitStartLeft = [start[0]+(10*unit[1]),start[1]-(10*unit[0])]
    perpUnitStartRright = [start[0]-(10*unit[1]),start[1]+(10*unit[0])]

    perpUnitEndLeft = [end[0]+(10*unit[1]),end[1]-(10*unit[0])]
    perpUnitEndRight = [end[0]-(10*unit[1]),end[1]+(10*unit[0])]

    return [perpUnitStartLeft,perpUnitStartRright,perpUnitEndLeft,perpUnitEndRight]

# Calculates the points that create vectors of 10 units extending perpendicularly from the endpoints
def calculateEndPerpendiculars(start,control0,control1,end):
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
def calculateUnitPerpendiculars(start,control0,control1,end):
        unitC00 = VectMath.unitvect([control0[0]-start[0],control0[1]-start[1]])
        perpUnitStartLeft = [0+unitC00[1],0-unitC00[0]]
        perpUnitStartRright = [0-unitC00[1],0+unitC00[0]]

        unitC01 = VectMath.unitvect([control1[0]-end[0],control1[1]-end[1]])
        perpUnitEndLeft = [0-unitC01[1],0+unitC01[0]]
        perpUnitEndRight = [0+unitC01[1],0-unitC01[0]]

        return [perpUnitStartLeft,perpUnitStartRright,perpUnitEndLeft,perpUnitEndRight]

# Calculates the bezier curves for the edges of the road.
def calculateLaneBeziers(start,control0,control1,end):
        perpendiculars = calculateEndPerpendiculars(start,control0,control1,end)
        SLP = [perpendiculars[0][0],perpendiculars[0][1]]
        SRP = [perpendiculars[1][0],perpendiculars[1][1]]
        ELP = [perpendiculars[2][0],perpendiculars[2][1]]
        ERP = [perpendiculars[3][0],perpendiculars[3][1]]

        unitPerps = calculateUnitPerpendiculars(start,control0,control1,end)
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
def debugDraw(screen,start,control00,control01,end):
        # Perpendiculars at the ends
        perpendiculars = calculateEndPerpendiculars(start,control00,control01,end)
        SLP = [perpendiculars[0][0],perpendiculars[0][1]]
        SRP = [perpendiculars[1][0],perpendiculars[1][1]]
        ELP = [perpendiculars[2][0],perpendiculars[2][1]]
        ERP = [perpendiculars[3][0],perpendiculars[3][1]]

        pygame.draw.aaline(screen,(255,0,0),start,SLP)
        pygame.draw.aaline(screen,(0,255,0),start,SRP)
        pygame.draw.aaline(screen,(255,0,0),end,ELP)
        pygame.draw.aaline(screen,(0,255,0),end,ERP)
        pygame.draw.aaline(screen,(0,0,255),start,control00)
        pygame.draw.aaline(screen,(255,0,0),end,control01)

        # Unit Perpendiculars for calculating beziers for lanes.
        unitPerps = calculateUnitPerpendiculars(start,control00,control01,end)
        uSLP = [unitPerps[0][0],unitPerps[0][1]]
        uSRP = [unitPerps[1][0],unitPerps[1][1]]
        uELP = [unitPerps[2][0],unitPerps[2][1]]
        uERP = [unitPerps[3][0],unitPerps[3][1]]
        SLPControl = [control00[0]+uSLP[0]*10+uELP[0]*10,control00[1]+uSLP[1]*10+uELP[1]*10]
        SRPControl = [control00[0]+uSRP[0]*10+uERP[0]*10,control00[1]+uSRP[1]*10+uERP[1]*10]
        ELPControl = [control01[0]+uSLP[0]*10+uELP[0]*10,control01[1]+uSLP[1]*10+uELP[1]*10]
        ERPControl = [control01[0]+uSRP[0]*10+uERP[0]*10,control01[1]+uSRP[1]*10+uERP[1]*10]

        # Bezier Control Lines
        pygame.draw.aaline(screen,(0,0,255),SLP,SLPControl)
        pygame.draw.aaline(screen,(0,0,255),SRP,SRPControl)
        pygame.draw.aaline(screen,(255,0,0),ELP,ELPControl)
        pygame.draw.aaline(screen,(255,0,0),ERP,ERPControl)