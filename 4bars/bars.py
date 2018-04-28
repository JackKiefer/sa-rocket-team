import matplotlib.lines as mlines
from matplotlib import collections as mc
import matplotlib.pyplot as plt
import numpy as np
import math

a = 1.704
c = 1.960
b = 1.656
d = 1.651

l = 0.875

# Force due to drag
Fd = 270

# Force due to tension
Ft = 223

point0A = (0,0)
pointAB = (0, -a)
pointD0 = (l,0)

pointBC = (float('nan'),float('nan'))


##########################
### Begin computations ###
##########################

def pointDistance((x1, y1), (x2, y2)):
    return np.sqrt((x2 - x1)**2 + (y1 - y2)**2)

def findIntersections(theta,pointCD):
    distance = pointDistance(pointAB, pointCD)
    nan = float('nan')
    if distance.any() > (b + c):
        print "No solutions; circles separate"
        return [(nan,nan),(nan,nan)]
    elif distance.any() < abs(b - c):
        print "No solutions; one circle is contained within the other"
        return [(nan,nan),(nan,nan)]
    elif distance.any() == 0 and b == c:
        print "Infinite solutions"
        return [(nan,nan),(nan,nan)]
    
    bbase  = (b**2 - c**2 + distance**2)/(2*distance)
    height = np.sqrt(b**2 - bbase**2)

    x2 = pointAB[0] + bbase*(pointCD[0]-pointAB[0])/distance
    y2 = pointAB[1] + bbase*(pointCD[1]-pointAB[1])/distance

    p1x = x2 + height*(pointCD[1]-pointAB[1])/distance
    p1y = y2 - height*(pointCD[0]-pointAB[0])/distance

    p2x = x2 - height*(pointCD[1]-pointAB[1])/distance
    p2y = y2 + height*(pointCD[0]-pointAB[0])/distance

    return [(p1x, p1y), (p2x, p2y)]

# Compute the location of points CD and BC
def getPoints(theta0):
    theta = 90 - theta0
    pointCD = (d*np.cos(np.radians(-theta))+l,d*np.sin(np.radians(-theta)))
    [(p1x, p1y), (p2x, p2y)] = findIntersections(theta,pointCD)
    pointBC = (0,0)
    if min(p1y.any(),p2y.any()) == p1y.any():
        pointBC = (p1x,p1y)
    else:
        pointBC = (p2x,p2y)
    return (pointCD, pointBC)

def slope((x1, y1), (x2, y2)):
    return (y2-y1)/(x2-x1)

def angleFromSlopes(m1, m2):
    n = m1 - m2
    d = 1 + m1*m2
    return np.degrees(np.arctan(n/d))

def lbfInchToNewtonMeter(x):
    return x * 0.112984829 

# Moment due to tension about the hinge CD
def tensionMoment((pointCD, pointBC)):    
    m1 = slope(pointBC, (l/2.0,0)) 
    m2 = slope(pointBC, pointCD) 
    degAngle = angleFromSlopes(m1, m2)
    return lbfInchToNewtonMeter(Ft*c*np.sin(np.radians(degAngle)))

# Moment due to drag about the hinge CD
def dragMoment(theta0):
    return lbfInchToNewtonMeter(Fd*(np.sin(np.radians(-theta0)))**2)
