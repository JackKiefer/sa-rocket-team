from scipy.optimize import fsolve
from matplotlib import collections as mc
import matplotlib.pyplot as plt
import numpy as np
import math

a = 2.191
b = 2.520
c = 2.120
d = 2.123

l = 1.125

# Force due to drag
Fd = 2.7

# Force due to tension
Ft = 2.23

point0A = (0,0)
pointAB = (0, -a)

pointBC = (float('nan'),float('nan'))


##########################
### Begin computations ###
##########################

def findIntersections(theta,pointCD):
    distance = math.sqrt((pointCD[0] - pointAB[0])**2 + (pointAB[1]-pointCD[1])**2)
    nan = float('nan')
    if distance > (b + c):
        print "No solutions; circles separate"
        return [(nan,nan),(nan,nan)]
    elif distance < abs(b - c):
        print "No solutions; one circle is contained within the other"
        return [(nan,nan),(nan,nan)]
    elif distance == 0 and b == c:
        print "Infinite solutions"
        return [(nan,nan),(nan,nan)]
    
    bbase  = (b**2 - c**2 + distance**2)/(2*distance)
    height = math.sqrt(b**2 - bbase**2)

    x2 = pointAB[0] + bbase*(pointCD[0]-pointAB[0])/distance
    y2 = pointAB[1] + bbase*(pointCD[1]-pointAB[1])/distance

    p1x = x2 + height*(pointCD[1]-pointAB[1])/distance
    p1y = y2 - height*(pointCD[0]-pointAB[0])/distance

    p2x = x2 - height*(pointCD[1]-pointAB[1])/distance
    p2y = y2 + height*(pointCD[0]-pointAB[0])/distance

    return [(p1x, p1y), (p2x, p2y)]

# Moment due to tension about the hinge D0
def tensionMoment(theta0):
    theta = 90 - theta0
    pointCD = (d*math.cos(math.radians(-theta))+l,d*math.sin(math.radians(-theta)))

    [(p1x, p1y), (p2x, p2y)] = findIntersections(theta,pointCD)

    pointBC = (0,0)
    if min(p1y,p2y) == p1y:
        pointBC = (p1x,p1y)
    else:
        pointBC = (p2x,p2y)

    # Perpendicular distance between BC and D0
    Dp = abs(pointBC[0] - l)
    return (Ft*Dp, pointCD, pointBC)

# Moment due to drag about the hinge D0
def dragMoment(theta0):
    theta = 90 - theta0 
    return Fd*(math.sin(math.radians(-theta)))**2

theta = 60
Mt, pointCD, pointBC = tensionMoment(theta)
Md = dragMoment(theta)

print "Mt",Mt
print "Md",Md


# Graphing
p = np.linspace(-3.0, 5,100)
q = np.linspace(-7.0, 1, 100)
X, Y = np.meshgrid(p,q)
F = X**2 + (Y+a)**2 - b**2
G = (X-(d*math.cos(math.radians(-theta))+l))**2 + (Y-(d*math.sin(math.radians(-theta))))**2 - c**2
plt.contour(X,Y,F,[0],linestyles="dotted")
plt.contour(X,Y,G,[0],linestyles="dotted")


plt.plot(0,0, 'bo')
plt.annotate("0A",(0,0),(0.1,0.1))

plt.plot(l,0, 'bo')
plt.annotate("D0",(l,0),(l+0.1,0.1))

plt.plot(pointAB[0],pointAB[1], 'bo')
plt.annotate("AB",pointAB, (pointAB[0]+0.1,pointAB[1]+0.1))

plt.plot(pointCD[0],pointCD[1],'bo')
plt.annotate("CD",pointCD, (pointCD[0]+0.1,pointCD[1]+0.1))

lines = [(0,pointAB[0]),(0,pointAB[1]),'b',
         (pointAB[0],pointBC[0]),(pointAB[1],pointBC[1]),'b',
         (l,pointCD[0]),(0,pointCD[1]),'b',
         (pointCD[0],pointBC[0]),(pointCD[1],pointBC[1]),'b',
         (l,l),(0,-0.3),'k']

plt.plot(pointBC[0],pointBC[1], 'ro')
plt.annotate("BC",pointBC, (pointBC[0]+0.1,pointBC[1]+0.1))

plt.annotate(r'$\Theta$ = '+str(theta), (l+0.1,-0.1))

plt.plot(*lines)

plt.show()
