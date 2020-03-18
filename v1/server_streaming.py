"""
aplikasi untuk uji coba streaming gambar

"""

import socket
import cv2
import os
import threading

# memgimport custom function
from streaming.v1 import streaming_function


# deklarasi semua fungsi yang build-in
class function:
    def list_client(self, s):
        while variable.proses:
            sc, address = s.accept()
            variable.list_cliet.append((sc, address))

    def sand_img(self, img_bytes, sc, size_file):

        # membuat header
        header = str(size_file).encode()
        sc.send(header)

        bit = img_bytes.read(1024)
        while bit:
            sc.send(bit)
            bit = img_bytes.read(1024)

        msg = "finish"
        sc.send(msg.encode())

# deklarasi variable yang akan digunakan
class variable:
    chache = "chace/chache.png"
    proses = True
    list_cliet = []

# memulai camera
cp = cv2.VideoCapture(0)

# membuka socket yang akan digunakan
s = socket.socket()
s.bind(("localhost", 9000))
s.listen(5)

# memulai thread untuk menangkap setiap client yang ada
threading.Thread(target=function().list_client, args=(s, )).start()

while True:
    _, img = cp.read()
    img = streaming_function.flip_img(img).start()
    cv2.imshow("kamera", img)

    # menyimpan gambar untuk chahe
    cv2.imwrite("chace/chache.png", img)

    # mulai mengirim gambar keclient yang terhubung
    if len(variable.list_cliet) > 0:
        print("send_gambar")
        # membaca gambar yang akan dikirim
        file = open(variable.chache, 'rb')
        size_file = os.path.getsize(variable.chache)

        thread = []
        for sc in variable.list_cliet:
            thread.append(threading.Thread(target=function().sand_img, args=(file, sc[0], size_file)))

        # memulai mengirim file
        for t in thread:
            t.start()
            t.join()

    k = cv2.waitKey(10)
    if k == ord('q'):
        cv2.destroyAllWindows()
        cp.release()
        variable.proses = False
        s.close()
        break