import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import numpy as np
from bars import *

############################
## Moment/Torque Graphing ##
############################

# Some evolved bar lengths
#evolved = [2.430908450433959, 2.057512651784845, 2.413864761792948, 2.2052046004836257]
#evolved = [2.0644872445326987, 0.27149729281069274, 1.7645929292997797, 3.0836095531942354]
evolved = [
    3.014326471905318, 2.287340174692796, 2.9931922963542696,
    2.4195053111602682
]

# Set up the "bars" dict to pass to needed functions
bars = {}
bars['a'] = evolved[0]
bars['b'] = evolved[1]
bars['c'] = evolved[2]
bars['d'] = evolved[3]

# Plot the drag moments
theta = np.arange(0, 90, 0.2)
dragMoments = dragMoment(theta).astype(np.float)
plt.plot(theta, dragMoments, 'r--', label='Moment due to drag')

# Plot the tension moments
tensionMoments = []
for angle in theta:
    tensionMoments.append(tensionMoment(getPoints(angle, bars), bars))
plt.plot(theta, tensionMoments, 'b', label='Optimized moment due to tension')

# Set up original (unoptimized) bar lengths
barsO = {}
barsO['a'] = 1.704
barsO['b'] = 1.656
barsO['c'] = 1.960
barsO['d'] = 1.651

# Plot the original tension moments
origTensionMoments = []
for angle in theta:
    origTensionMoments.append(tensionMoment(getPoints(angle, barsO), barsO))
plt.plot(
    theta, origTensionMoments, 'g', label='Original moment due to tension')

# Plot the difference between the original and optimized tension moments with the drag moments
#origDif = origTensionMoments - dragMoments
#optiDif = tensionMoments - dragMoments
#plt.plot(theta, origDif, 'g--', label='Original torque difference')
#plt.plot(theta, optiDif, 'b--', label='Optimized torque difference')

# Manually construct the legend
red_line = mlines.Line2D([], [], color='r', label='Moment due to drag')
blue_line = mlines.Line2D(
    [], [], color='b', label='Optimized moment due to tension')
green_line = mlines.Line2D(
    [], [], color='g', label='Original moment due to tension')
plt.legend(handles=[red_line, blue_line, green_line])

# Final plot setup
plt.title("Moments about the hinge point")
plt.xlabel("Air Brake angle (degrees)")
plt.ylabel("Moment (newton metres)")
plt.grid()
plt.show()

##############################################
## Static diagram of the system at theta=60 ##
##############################################

theta = 60
pointCD, pointBC = getPoints(theta, bars)
pointAB = (0, -bars['a'])

# Plot the points and label them

plt.plot(0, 0, 'bo')
plt.annotate("0A", (0, 0), (0.1, 0.1))

plt.plot(l, 0, 'bo')
plt.annotate("D0", (l, 0), (l + 0.1, 0.1))

plt.plot(pointAB[0], pointAB[1], 'bo')
plt.annotate("AB", pointAB, (pointAB[0] + 0.1, pointAB[1] + 0.1))

plt.plot(pointCD[0], pointCD[1], 'bo')
plt.annotate("CD", pointCD, (pointCD[0] + 0.1, pointCD[1] + 0.1))

# Plot the lines

lines = [(0, pointAB[0]), (0, pointAB[1]), 'b', (pointAB[0], pointBC[0]),
         (pointAB[1], pointBC[1]), 'b', (l, pointCD[0]), (0, pointCD[1]), 'b',
         (pointCD[0], pointBC[0]), (pointCD[1],
                                    pointBC[1]), 'b', (l, l), (0, -0.3), 'k']

plt.plot(pointBC[0], pointBC[1], 'ro')

plt.annotate("BC", pointBC, (pointBC[0] + 0.1, pointBC[1] + 0.1))

# Label the lines
plt.annotate("$a$", (pointAB[0] / 2 + 0.1, pointAB[1] / 2))
plt.annotate("$b$",
             (pointAB[0] + ((pointBC[0] - pointAB[0]) / 2.0), pointAB[1] +
              ((pointBC[1] - pointAB[1]) / 2.0) + 0.1))
plt.annotate(
    "$c$", (pointBC[0] + ((pointCD[0] - pointBC[0]) / 2.0 - 0.1), pointBC[1] +
            ((pointCD[1] - pointBC[1]) / 2.0)))
plt.annotate("$d$", (((l + pointCD[0]) / 2.0), pointCD[1] / 2.0 + 0.1))

# Add the angle indicator
plt.annotate(r'$\Theta$ = ' + str(theta), (1.5, 0))

# And plot!
plt.plot(*lines)
plt.show()
