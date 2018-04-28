import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import bars as b

# create a time array from 0..100 sampled at 0.05 second steps
dt = 1
t0 = np.array([0, 0, 0, 0, 0, 0,0,0,0, 0])
t1 = np.arange(0.0, 90, dt)
t2 = np.array([90, 90, 90, 90, 90, 90, 90, 90, 90, 90])
t3 = np.arange(90.0,0.0,-dt)
t = np.concatenate((t0,t1, t2,t3),axis=0)

x1 = np.copy(t)
y1 = np.copy(t)

x2 = np.copy(t)
y2 = np.copy(t)

for i in range(0,len(t)):
    p1, p2 = b.getPoints(t[i])
    # p1 = CD
    # p2 = BC
    x1[i] = p1[0]
    y1[i] = p1[1]
    x2[i] = p2[0]
    y2[i] = p2[1]

fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-1, 4), ylim=(-4.5, 0.5))
ax.grid()

line, = ax.plot([], [], 'o-', color="#fc6602", lw=2)
cable, = ax.plot([],[], 'k:', lw=2)
airbrake, = ax.plot([],[],'#0298fc', lw=5)

rightline, = ax.plot([b.l,b.l],[-2*b.d-0.02,-3*b.d],'#0298fc', lw=5)
upline,    = ax.plot([b.l,b.l],[0,1],'#0298fc', lw=5)

time_template = '$\Theta$ = %.1f degrees'
time_text = ax.text(0.05, 0.95, '', transform=ax.transAxes)


def init():
    line.set_data([], [])
    cable.set_data([],[])
    airbrake.set_data([],[])
    time_text.set_text('')
    return line, time_text


def animate(i):
    thisx = [0, 0,    x2[i], x1[i], b.l]
    thisy = [0, -b.a, y2[i], y1[i],   0]

    line.set_data(thisx, thisy)
    cable.set_data([b.l/2, x2[i]],[0,y2[i]])

    xdistance = x1[i] - b.l

    airbrake.set_data([b.l, b.l + (x1[i]-b.l)*2 ],[0, y1[i]*2])

    time_text.set_text(time_template % (t[i]))
    return airbrake, line, cable, time_text

ani = animation.FuncAnimation(fig, animate, np.arange(1, len(t)),
                              interval=25, blit=True, init_func=init, repeat=True)

# ani.save('fourbar.mp4', fps=24)

plt.show()

