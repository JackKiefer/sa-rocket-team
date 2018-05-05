import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import bars as b

# Set the bar lengths here
#evolved = [2.430908450433959, 2.057512651784845, 2.413864761792948, 2.2052046004836257]
#evolved = [3.014326471905318, 2.287340174692796, 2.9931922963542696, 2.4195053111602682]
evolved = [
    3.014326471905318, 2.6573598481473786, 2.9931922963542696,
    2.789639454558845
]

# Optionally set them here
bars = {}
#bars['a'] = 1.704
#bars['b'] = 1.656
#bars['c'] = 1.960
#bars['d'] = 1.651

bars['a'] = evolved[0]
bars['b'] = evolved[1]
bars['c'] = evolved[2]
bars['d'] = evolved[3]

# create a time array from 0..100 sampled at 0.05 second steps
dt = 1
t0 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
t1 = np.arange(0.0, 90, dt)
t2 = np.array([90, 90, 90, 90, 90, 90, 90, 90, 90, 90])
t3 = np.arange(90.0, 0.0, -dt)
t = np.concatenate((t0, t1, t2, t3), axis=0)

x1 = np.copy(t)
y1 = np.copy(t)

x2 = np.copy(t)
y2 = np.copy(t)

# Set the time-series appropriately
for i in range(0, len(t)):
    p1, p2 = b.getPoints(t[i], bars)
    x1[i] = p1[0]
    y1[i] = p1[1]
    x2[i] = p2[0]
    y2[i] = p2[1]

# Figure setup
fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-1, 6), ylim=(-6.5, 0.5))
ax.set_aspect('equal')
ax.grid()

# Main 4-bar system
line, = ax.plot([], [], 'o-', color="#fc6602", lw=2)

# Tension cable
cable, = ax.plot([], [], 'k:', lw=2)

# Airbrake flap
airbrake, = ax.plot([], [], '#0298fc', lw=5)

# Other "sides" of the rocket
rightline, = ax.plot(
    [b.l, b.l], [-2 * bars['d'] - 0.02, -3 * bars['d']], '#0298fc', lw=5)
upline, = ax.plot([b.l, b.l], [0, 1], '#0298fc', lw=5)

# Show what the angle is
time_template = '$\Theta$ = %.1f degrees'
time_text = ax.text(0.05, 0.95, '', transform=ax.transAxes)


def init():
    line.set_data([], [])
    cable.set_data([], [])
    airbrake.set_data([], [])
    time_text.set_text('')
    return line, time_text


def animate(i):
    # Update the 4-bar system
    thisx = [0, 0, x2[i], x1[i], b.l]
    thisy = [0, -bars['a'], y2[i], y1[i], 0]
    line.set_data(thisx, thisy)

    # Update the cable
    cable.set_data([b.l / 2, x2[i]], [0, y2[i]])

    # Update the airbrake flap
    xdistance = x1[i] - b.l
    airbrake.set_data([b.l, b.l + (x1[i] - b.l) * 2], [0, y1[i] * 2])

    # Update the theta
    time_text.set_text(time_template % (t[i]))

    # Just... Return everything, I guess
    return airbrake, line, cable, time_text


# Animate it!
ani = animation.FuncAnimation(
    fig,
    animate,
    np.arange(1, len(t)),
    interval=25,
    blit=True,
    init_func=init,
    repeat=True)

# Save as a nice .mp4
#ani.save('fourbar.mp4', fps=24)

plt.show()
