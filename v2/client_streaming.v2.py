"""
aplikasi streaming client v2
"""

import socket, pickle, cv2, threading, re
import numpy as np

# class untuk menampung variable yang akan digunakan
class variable:
    ip = "localhost"
    port = 9000
    proses = True
    list_img = ""
    finish = re.compile(rb'finish')
    show_img = []
    show_id = 0

# class untuk menampung function buil in
class function:

    # fungsi untuk menerima gambar dari server
    def recv_img(self, s):
        while variable.proses:
            # menerima header dari server
            try:
                header = int(s.recv(1024).decode())
            except:
                header = False

            # cek apakah header bisa dibaca
            if header:
                # membaca semua bit
                bit = s.recv(1024)
                img_array = b''
                while bit and variable.proses:
                    # cek apakah ada sintak finish
                    if variable.finish.search(bit):
                        print(bit)
                        bit = bit.split(b'finish')
                        img_array += bit[0]
                        break
                    else:
                        print(bit)
                        img_array += bit
                        bit = s.recv(1024)

                try:
                    img_array = pickle.loads(img_array)
                    variable.list_img = np.array(img_array)
                    variable.show_id += 1
                except:
                    None


# deklarasi port dan ip addres dari server
s = socket.socket()
s.connect((variable.ip, variable.port))

# memulai thread untuk menerima setiap gambar
threading.Thread(target=function().recv_img, args=(s, )).start()

# mulai menampilkan gambar
while variable.proses:
    if len(variable.list_img) > 0:
        cv2.imshow("client", variable.list_img)
        if cv2.waitKey(10) == ord('q'):
            cv2.destroyAllWindows()
            s.close()
            variable.proses = False
            break
    else:
        print("Buffer belum terisi")