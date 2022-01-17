import socket
import struct

s = socket.socket(type=socket.SOCK_DGRAM)
s.bind(('192.168.4.2', 9999))

# while True:
#     csi, address = s.recvfrom(16)
#     csi = struct.unpack('4f', csi)
#
#     csi_mod = pow(csi[0], 2)+pow(csi[1], 2)
#
#     print(csi_mod, csi)
cnt = 0
with open('touchTest.dat', 'wb') as f:
        while (cnt < 2000):
            cnt += 1
            data, address = s.recvfrom(16)
            csi = struct.unpack('4f', data)
            f.write(data)
            print(cnt)
        print('end')