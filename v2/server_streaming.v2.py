"""
aplikasi streaming gambar versi 2

for server
"""

import socket, pickle, cv2, threading
import numpy as np


# semua variable yang akan digunakan didalam aplikasi
class variable:
    ip = "localhost"
    port = 9000
    proses = True
    list_client = []


# semua function yang akan digunakan
class function:

    # fungsi untuk mendata semua client yang sedang terhubung
    def list_client(self, s):
        while variable.proses:
            sc, address = s.accept()
            variable.list_client.append(sc)

    # fungsi untuk mengirim file ke client yang sudah terhubung
    def send_img(self, sc, img):
        size_img = img.__sizeof__()

        # membuat header sebagai pertanda awalan file
        header = str(size_img)
        try:
            sc.send(header.encode())  # mengirim header ke client
        except:
            print("gagal mengirim header")
            variable.list_client.remove(sc)

        # mulai mengirim setiap bytes
        try:
            sc.send(img)
        except:
            print("gagalm mengirim gambar")
            variable.list_client.remove(sc)

        # membuat footer untuk menandai akhir dari gambar
        footer = b'finish'
        try:
            sc.send(footer)
        except:
            print("gagal mengirim footer")
            variable.list_client.remove(sc)

class streaming_function:
    class flip_img:
        def __init__(self, img):
            self.img = img
            self.img_array = np.array(img)

        def start(self):
            img_save = list(map(lambda data_array: np.flipud(data_array), self.img_array))
            return np.array(img_save)

# deklarasi socket untuk server
s = socket.socket()
s.bind((variable.ip, variable.port))
s.listen()

# memulai thread untuk mendata semua client yang terhubung
threading.Thread(target=function().list_client, args=(s, )).start()

# mulai menangkap gambar dari web cam
cp = cv2.VideoCapture(0)

while cp.isOpened():

    # memangambil gambar dari kamera
    _, img = cp.read()
    img = streaming_function.flip_img(img).start()

    # menampilkan gambar yang sedang direkam
    cv2.imshow("kamera", img)

    # merubah gambar dari array ke bytes
    img_bytes = pickle.dumps(img)

    # mengirimkan gambar ke setiap client yang tehubung
    for client in variable.list_client:
        t = threading.Thread(target=function().send_img, args=(client, img_bytes))
        t.start()
        t.join()


    if cv2.waitKey(10) == ord('q'):
        cp.release()
        s.close()
        cv2.destroyAllWindows()
        variable.proses = False
        break