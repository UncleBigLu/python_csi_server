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

# Average window size
N = 200
l_real_data = []
l_img_data = []
ht_real_data = []
ht_img_data = []
# Low pass filter window size
LPF = 40
l_real_filter = []
l_img_filter = []
ht_real_filter = []
ht_img_filter = []
l_real_sum = 0
l_img_sum = 0
ht_real_sum = 0
ht_img_sum = 0
e_l_img, e_l_real, e_ht_img, e_ht_real = 0,0,0,0
# Covariance between lltf and htltf
std_real, std_img = 0, 0

# Get csi from udp socket
def get_csi():
    for i in itertools.count():
        csi, address = s.recvfrom(16)
        csi = struct.unpack('4f', csi)
        yield i, csi

def init():
    # Set the y-axis view limits
    ax.set_ylim(-5, 10)
    ax.set_xlim(0, 1000)
    del xdata[:]
    del ydata[:]
    line.set_data(xdata, ydata)

def run(data):
    t, csi = data
    l_img, l_real, ht_img, ht_real = csi
    global l_real_sum, l_img_sum, ht_img_sum, ht_real_sum
    global e_l_img, e_l_real, e_ht_img, e_ht_real

    l_real_filter.append(l_real)
    l_img_filter.append(l_img)
    ht_real_filter.append(ht_real)
    ht_img_filter.append(ht_img)

    l_real_sum += l_real
    l_img_sum += l_img
    ht_img_sum += ht_img
    ht_real_sum += ht_real


    if(len(l_img_filter) < LPF):
        return


    l_img_data.append(l_img_sum / LPF)
    l_real_data.append(l_real_sum / LPF)
    ht_img_data.append(ht_img_sum / LPF)
    ht_real_data.append(ht_real_sum / LPF)

    e_l_img += l_img_data[-1] / N
    e_l_real += l_real_data[-1] / N
    e_ht_img += ht_img_data[-1] / N
    e_ht_real += ht_real_data[-1] / N


    l_real_sum -= l_real_filter.pop(0)
    l_img_sum -= l_img_filter.pop(0)
    ht_real_sum -= ht_real_filter.pop(0)
    ht_img_sum -= ht_img_filter.pop(0)

    if(len(l_img_data) < N):
        return

    global std_img, std_real
    std_img, std_real = 0, 0
    for i in range(0, N):
        std_img += (l_img_data[i] - e_l_img)*(ht_img_data[i] - e_ht_img) / N
        std_real += (l_real_data[i] - e_l_real)*(ht_real_data[i] - e_ht_real) / N


    e_l_img -= (l_img_data.pop(0) / N)
    e_l_real -= (l_real_data.pop(0) / N)
    e_ht_img -= (ht_img_data.pop(0) / N)
    e_ht_real -= (ht_real_data.pop(0) / N)


    xdata.append(t)

    ydata.append(l_real_sum/LPF)
    print(csi)

    xmin, xmax = ax.get_xlim()
    if(len(xdata) > xmax):
        del xdata[:800]
        del ydata[:800]
        ax.set_xlim(xmin+800, xmax+800)
        ax.figure.canvas.draw()
    line.set_data(xdata, ydata)
    return line

if __name__ == '__main__':
    ani = animation.FuncAnimation(fig, run, get_csi, interval=1, init_func=init)
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
