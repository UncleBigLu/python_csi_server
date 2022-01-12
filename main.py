import socket
import struct

import itertools

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


s = socket.socket(type=socket.SOCK_DGRAM)
s.bind(('192.168.4.2', 9999))

cnt = 0

# Create a figure and a set of subplots.
# Returns: figure, axes.Axes or Array of Axes
# Figures: windows, widgets
# Figure contains one or more Axes
# Axes: an area where points can be specified in terms of x-y coordinates
fig, ax = plt.subplots()
# lw: line width
line, = ax.plot([], [], lw=2)
ax.grid()
xdata, ydata = [], []

# Get csi from udp socket
def get_csi():
    for i in itertools.count():
        csi, address = s.recvfrom(4)
        csi = struct.unpack('f', csi)[0]
        yield i, csi

def init():
    # Set the y-axis view limits
    ax.set_ylim(35, 70)
    ax.set_xlim(0, 100)
    del xdata[:]
    del ydata[:]
    line.set_data(xdata, ydata)

def run(data):
    t, y = data
    xdata.append(t)
    ydata.append(y)
    xmin, xmax = ax.get_xlim()
    if(len(xdata) > xmax):
        xdata.pop()
        ydata.pop()
        ax.set_xlim(xmin+1, xmax+1)
        ax.figure.canvas.draw()
    line.set_data(xdata, ydata)
    return line

if __name__ == '__main__':
    ani = animation.FuncAnimation(fig, run, get_csi, interval=2, init_func=init)
    plt.show()
    # with open('csi2.dat', 'wb') as f:
    #     while (cnt < 1000):
    #         cnt += 1
    #         data, address = s.recvfrom(4)
    #         d = struct.unpack('f', data)[0]
    #         f.write(data)
    #         print(d)
    #         print(cnt)
    #     print('end')
