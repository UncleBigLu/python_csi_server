import struct
import matplotlib.pyplot as plt
import numpy as np

l = []

with open('csi.dat', 'rb') as f:
    cnt = 0
    while cnt < 1000:
        cnt += 1
        data = f.read(4)
        d = struct.unpack('f', data)[0]
        l.append(d)

x = np.arange(0, 1000)

l1 = plt.plot(x, l)
plt.show()
