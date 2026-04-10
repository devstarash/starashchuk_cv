import numpy as np
import socket 
from skimage.measure import label
host = "84.237.21.36"
port = 5152
def recvall(sock, amount_of_bytes):
    data = bytearray()
    while(len(data) < amount_of_bytes):
        packet = sock.recv(amount_of_bytes - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data
        
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))
    sock.send(b"124ras1")
    sock.recv(10)
    beat = b'nope'
    while beat != b'yep':
        sock.send(b"get")
        resp = recvall(sock, 40002)
        image = np.frombuffer(resp[2:], dtype = "uint8")
        image = image.reshape(resp[1], resp[0])
        labeled = image.copy()
        labeled = np.where(labeled > 150, 1, 0)
        labeled = label(labeled)
        fig2 = image.copy()
        fig1 = image.copy()
        fig1[labeled != 1] = 0
        fig2[labeled != 2] = 0
        y1, x1 = np.where(fig1 == fig1.max())[0][0], np.where(fig1 == fig1.max())[1][0]
        y2, x2 = np.where(fig2 == fig2.max())[0][0], np.where(fig2 == fig2.max())[1][0]
        dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        dist = round(dist, 1)
        sock.send(f"{dist}".encode())
        resp = (sock.recv(10))
        print(resp)
        sock.send(b"beat")
        beat = sock.recv(10)
    print("Задача решена")

        
