import struct
import matplotlib.pyplot as plt
import numpy as np

l_img = []
l_real = []
ht_img = []
ht_real = []

fig, axs = plt.subplots(4)

with open('touchTest.dat', 'rb') as f:
    cnt = 0
    while cnt < 2000:
        cnt += 1
        data = f.read(16)
        csi = struct.unpack('4f', data)
        l_img.append(csi[0])
        l_real.append(csi[1])
        ht_img.append(csi[2])
        ht_real.append(csi[3])

x = np.arange(0, 2000)

axs[0].plot(x, l_img, label="l_img")
axs[1].plot(x, l_real, label="l_real")
axs[2].plot(x, ht_img, label="ht_img")
axs[3].plot(x, ht_real, label="ht_real")
plt.legend()

plt.show()
