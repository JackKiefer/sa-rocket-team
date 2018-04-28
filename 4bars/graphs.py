import matplotlib.lines as mlines
from matplotlib import collections as mc
import matplotlib.pyplot as plt
import numpy as np
import math
from bars import *

theta = np.arange(0,90,0.2)
plt.plot(theta, dragMoment(theta).astype(np.float), 'r--', label='Moment due to drag')

tensionMoments = []
for angle in theta:
    tensionMoments.append(tensionMoment(getPoints(angle)))

plt.plot(theta, tensionMoments, 'b', label='Moment due to tension')
#plt.plot((60,60),(0,3),'k:')

red_line = mlines.Line2D([],[],color='r',ls='dashed',label='Moment due to drag')
blue_line = mlines.Line2D([],[],color='b',label='Moment due to tension')
plt.legend(handles=[red_line,blue_line])

plt.title("Moments about the hinge point")
plt.xlabel("Air Brake angle (degrees)")
plt.ylabel("Moment (newton metres)")
plt.grid()
plt.show()

theta = 90
pointCD, pointBC = getPoints(theta)

# Graphing
#p = np.linspace(-3.0, 5,100)
#q = np.linspace(-7.0, 1, 100)
#X, Y = np.meshgrid(p,q)
#F = X**2 + (Y+a)**2 - b**2
#G = (X-(d*np.cos(np.radians(-theta))+l))**2 + (Y-(d*np.sin(np.radians(-theta))))**2 - c**2
#plt.contour(X,Y,F,[0],linestyles="dotted")
#plt.contour(X,Y,G,[0],linestyles="dotted")

plt.plot(0,0, 'bo')
#plt.annotate("0A",(0,0),(0.1,0.1))

plt.plot(l,0, 'bo')
#plt.annotate("D0",(l,0),(l+0.1,0.1))

plt.plot(pointAB[0],pointAB[1], 'bo')
#plt.annotate("AB",pointAB, (pointAB[0]+0.1,pointAB[1]+0.1))

plt.plot(pointCD[0],pointCD[1],'bo')
#plt.annotate("CD",pointCD, (pointCD[0]+0.1,pointCD[1]+0.1))

lines = [(0,pointAB[0]),(0,pointAB[1]),'b',
         (pointAB[0],pointBC[0]),(pointAB[1],pointBC[1]),'b',
         (l,pointCD[0]),(0,pointCD[1]),'b',
         (pointCD[0],pointBC[0]),(pointCD[1],pointBC[1]),'b',
         (l,l),(0,-0.3),'k']

plt.plot(pointBC[0],pointBC[1], 'ro')
#plt.annotate("BC",pointBC, (pointBC[0]+0.1,pointBC[1]+0.1))

plt.annotate("$a$",(pointAB[0]/2+0.1,pointAB[1]/2))
plt.annotate("$b$",(pointAB[0]+((pointBC[0]-pointAB[0])/2.0),pointAB[1]+((pointBC[1]-pointAB[1])/2.0)+0.1))
plt.annotate("$c$",(pointBC[0]+((pointCD[0]-pointBC[0])/2.0 -0.1),pointBC[1]+((pointCD[1]-pointBC[1])/2.0)))
plt.annotate("$d$",(((l+pointCD[0])/2.0), pointCD[1]/2.0 +0.1))

plt.annotate(r'$\Theta$ = '+str(theta), (1.5,0))

plt.plot(*lines)

plt.show()

