import matplotlib.lines as mlines
from matplotlib import collections as mc
import matplotlib.pyplot as plt
import numpy as np
import math

# Width of the rocket chamber (inches)
l = 0.875

# Force due to drag (lbf)
Fd = 270

# Force due to tension (lbf)
Ft = 223

point0A = (0,0)
pointD0 = (l,0)
pointBC = (float('nan'),float('nan'))

##########################
### Begin computations ###
##########################

# Calculate the distance between two points
def pointDistance((x1, y1), (x2, y2)):
    return np.sqrt((x2 - x1)**2 + (y1 - y2)**2)

# Find the intersection points of the two circles that define the range of
# motion for points BC and CD.
# Will return sets of NaN if the intersection points do not exist.
def findIntersections(theta, pointCD, bars):
    distance = pointDistance((0,-bars['a']), pointCD)
    nan = float('nan')
    if distance.any() > (bars['b'] + bars['c']):
#        print "No solutions; circles separate"
        return [(nan,nan),(nan,nan)]
    elif distance.any() < abs(bars['b'] - bars['c']):
#        print "No solutions; one circle is contained within the other"
        return [(nan,nan),(nan,nan)]
    elif distance.any() == 0 and bars['b'] == bars['c']:
#        print "Infinite solutions"
        return [(nan,nan),(nan,nan)]
    
    bbase  = (bars['b']**2 - bars['c']**2 + distance**2)/(2*distance)

    height = 0
    if bars['b']**2 - bbase**2 > 0:
        height = np.sqrt(bars['b']**2 - bbase**2)

    x2 = (0,-bars['a'])[0] + bbase*(pointCD[0]-(0,-bars['a'])[0])/distance
    y2 = (0,-bars['a'])[1] + bbase*(pointCD[1]-(0,-bars['a'])[1])/distance

    p1x = x2 + height*(pointCD[1]-(0,-bars['a'])[1])/distance
    p1y = y2 - height*(pointCD[0]-(0,-bars['a'])[0])/distance

    p2x = x2 - height*(pointCD[1]-(0,-bars['a'])[1])/distance
    p2y = y2 + height*(pointCD[0]-(0,-bars['a'])[0])/distance

    return [(p1x, p1y), (p2x, p2y)]

# Compute the location of points BC and CD
def getPoints(theta0, bars):
    theta = 90 - theta0
    pointCD = (bars['d']*np.cos(np.radians(-theta))+l,bars['d']*np.sin(np.radians(-theta)))
    [(p1x, p1y), (p2x, p2y)] = findIntersections(theta,pointCD, bars)
    pointBC = (0,0)
    if min(p1y,p2y) == p1y:
        pointBC = (p1x,p1y)
    else:
        pointBC = (p2x,p2y)
    return (pointCD, pointBC)

# Compute the slope between two points
def slope((x1, y1), (x2, y2)):
    return (y2-y1)/(x2-x1)

# Calculate an angle between two slopes
def angleFromSlopes(m1, m2):
    num = m1 - m2
    d = 1 + m1*m2
    return np.degrees(np.arctan(num/d))

# Convert lbf*inch to newton*meter
def lbfInchToNewtonMeter(x):
    return x * 0.112984829 

# Moment due to tension about the hinge CD.
# Returns -1000 when given bad data for optimization and graphing purposes.
def tensionMoment((pointCD, pointBC),bars,optimizing=False):    
    if np.isnan(pointCD[0]) or np.isnan(pointBC[0]):
        return -1000
    if optimizing and pointBC[0] < 0:
        return -1000
    m1 = slope(pointBC, (l/2.0,0)) 
    m2 = slope(pointBC, pointCD) 
    degAngle = angleFromSlopes(m1, m2)
    return lbfInchToNewtonMeter(Ft*bars['c']*np.sin(np.radians(degAngle)))

# Moment due to drag about the hinge CD
def dragMoment(theta0):
    return lbfInchToNewtonMeter(Fd*(np.sin(np.radians(-theta0)))**2)
