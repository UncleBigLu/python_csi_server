import socket
import struct

import itertools

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

q = []

# def data_gen():
#     for cnt in itertools.count():
#         t = cnt / 10
#         if(len(q) == 0):
#             yield t, 0
#         else:
#             v = q[0]
#             q.pop()
#             yield t, v
#
#
# def init():
#     ax.set_ylim(40, 70)
#     ax.set_xlim(0, 10)
#     del xdata[:]
#     del ydata[:]
#     line.set_data(xdata, ydata)
#     return line,
#
# fig, ax = plt.subplots()
# line, = ax.plot([], [], lw=2)
# ax.grid()
# xdata, ydata = [], []
#
#
# def run(data):
#     # update the data
#     t, y = data
#     xdata.append(t)
#     ydata.append(y)
#     xmin, xmax = ax.get_xlim()
#
#     if t >= xmax:
#         ax.set_xlim(xmin, 2*xmax)
#         ax.figure.canvas.draw()
#     line.set_data(xdata, ydata)
#
#     return line,
#
# ani = animation.FuncAnimation(fig, run, data_gen, interval=10, init_func=init)
# plt.show()



s = socket.socket(type=socket.SOCK_DGRAM)
s.bind(('192.168.4.2', 9999))

cnt = 0
with open('csi2.dat', 'wb') as f:
    while (cnt < 1000):
        cnt += 1
        data, address = s.recvfrom(4)
        d = struct.unpack('f', data)[0]
        f.write(data)
        print(d)
        print(cnt)
    print('end')





