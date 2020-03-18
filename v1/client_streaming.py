import socket
import cv2
import threading
import os

s = socket.socket()
s.connect(("localhost", 9000))

class variable:
    i = 0

if not os.path.exists("chace"):
    os.mkdir("chace")

# fungsi built in
class function:
    def recv_img(self, s):
        while True:
            file = open("chace_client/" + str(variable.i) + ".png", 'wb')
            try:
                size_file = int(s.recv(1024).decode())
            except:
                size_file = False

            if size_file:
                bit = s.recv(1024)
                while bit:
                    if bit == b'finish':
                        break

                    size_file -= 1024
                    file.write(bit)
                    if size_file >= 1024:
                        bit = s.recv(1024)
                    elif size_file > 0:
                        bit = s.recv(size_file)
                    else:
                        bit = s.recv(1024)

                file.close()
                variable.i += 1


# memulai thread
threading.Thread(target=function().recv_img, args=(s, )).start()

while True:

    img = cv2.imread("chace_client/" + str(variable.i) + ".png")
    try:
        cv2.imshow("client_streaming", img)
    except:
        None
    k = cv2.waitKey(10)
    if k == ord('q'):
        s.close()
        break
