###############
# VectMath.py
# Ian Watterson October 30,2015
# Function for vector math, some are from David Barker's Bezier Curves program.
#  http://www.pygame.org/project/1166/?release_id=2083
###############

import math

def vectadd(vecta,vectb):
    return (vecta[0]+vectb[0],vecta[1]+vectb[1])

def dist(a, b):
    return math.sqrt(abs((b[0]-a[0])*(b[0]-a[0])) + abs((b[1]-a[1])*(b[1]-a[1])))

def unitvect(vect):
    return [vect[0]/(math.sqrt((vect[0]*vect[0])+(vect[1]*vect[1]))),vect[1]/(math.sqrt((vect[0]*vect[0])+(vect[1]*vect[1])))]

def vectmult(num, vect):
    # Multiply two vectors
    return [num*vect[0], num*vect[1]]

# The following three functions are for summing vectorss
def twopointsum(a, b):
    return [a[0] + b[0], a[1] + b[1]]

def threepointsum(a, b, c):
    return[a[0] + b[0] + c[0], a[1] + b[1] + c[1]]

def fourpointsum(a, b, c, d):
    return[a[0] + b[0] + c[0] + d[0], a[1] + b[1] + c[1] + d[1]]