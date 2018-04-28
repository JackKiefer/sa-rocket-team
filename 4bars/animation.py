import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import bars as b

# create a time array from 0..100 sampled at 0.05 second steps
dt = 1
t1 = np.arange(0.0, 90, dt)
t2 = np.arange(90.0,0.0,-dt)
t = np.concatenate((t1, t2),axis=0)

x1 = np.copy(t)
y1 = np.copy(t)

x2 = np.copy(t)
y2 = np.copy(t)

for i in range(0,len(t)):
    p1, p2 = b.getPoints(t[i])
    x1[i] = p1[0]
    y1[i] = p1[1]
    x2[i] = p2[0]
    y2[i] = p2[1]

fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-1, 3), ylim=(-3.5, 0.5))
ax.grid()

line, = ax.plot([], [], 'o-', lw=2)
time_template = '$\Theta$ = %.1f degrees'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)


def init():
    line.set_data([], [])
    time_text.set_text('')
    return line, time_text


def animate(i):
    thisx = [0, 0,    x2[i], x1[i], b.l]
    thisy = [0, -b.a, y2[i], y1[i],   0]

    line.set_data(thisx, thisy)
    time_text.set_text(time_template % (t[i]))
    return line, time_text

ani = animation.FuncAnimation(fig, animate, np.arange(1, len(t)),
                              interval=25, blit=True, init_func=init, repeat=True)

# ani.save('fourbar.mp4', fps=24)

plt.show()

