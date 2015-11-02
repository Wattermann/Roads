###############
# Bezier.py
# Functions for computing a Bezier Curve. Majority is from David Barker's Bezier Curves program.
# http://www.pygame.org/project/1166/?release_id=2083
###############

import math
import pygame
import VectMath

# num^2
def sqr(num):
    return num*num

# num^3
def cube(num):
    return num*num*num

# Same as all GetAllBezierPoints(), but also draws.
def DrawBezier(points,screen,color):
    bezierpoints = []
    t = 0.0
    while t < 1.02:  # Increment through values of t (between 0 and 1)
        # Append the point on the curve for the current value of t to the list of Bezier points
        bezierpoints.append(GetBezierPoint(points, t))
        t += 0.02  # t++

    # Draw the curve
    pygame.draw.aalines(screen,color,False,bezierpoints)

# Returns the Bezier Points to be used in the pygame.draw.aalines() function.
def GetAllBezierPoints(points):
    bezierpoints = []
    t = 0.0
    while t < 1.02:  # Increment through values of t (between 0 and 1)
        # Append the point on the curve for the current value of t to the list of Bezier points
        bezierpoints.append(GetBezierPoint(points, t))
        t += 0.02  # t++

    return bezierpoints

# Gets the bezier points when provided with two points.
def GetBezierPoint(points, t):
    """EXPLANATION:
The formula for a point on the bezier curve defined by four points (points[0:3]) at a given value of t is as follows:
    B(t) = ((1-t)^3 * points[0]) + (3 * (1-t)^2 * t * points[1]) + (3 * (1-t) * t^2 * points[2]) + (t^3 * points[3])
            (Where 0 <= t <= 1.)

Here, the formula has been split into the four component parts, each returning a vactor:
    -part1 = (1-t)^3 * points[0]
    -part2 = 3 * (1-t)^2 * t * points[1]
    -part3 = 3 * (1-t) * t^2 * points[2]
    -part4 = t^3 * points[3]

These vectors are then added using the function fourpointsum() to give the final value for B(t).
    """
    part1 = VectMath.vectmult(cube(1.0 - t), points[0])
    part2 = VectMath.vectmult((3 * sqr(1.0 - t) * t), points[1])
    part3 = VectMath.vectmult((3 * (1.0 - t) * sqr(t)), points[2])
    part4 = VectMath.vectmult(cube(t), points[3])

    return VectMath.fourpointsum(part1, part2, part3, part4)