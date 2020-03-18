import cv2
import re
import pickle

file = open("v1/chace/chache.png", "rb")
baris = file.readline() + b'finish'
finish = re.compile(rb'finish')
text_finish = b'finish'
print(text_finish.split(b'finish'))
if finish.search(baris):
    print(baris)
    baris = baris.split(b'finish')
    print(baris[0])
    print("data ada")
else:
    print("tidak ada")

img = cv2.imread("v1/chace/chache.png")
img_bytes = pickle.dumps(img)
potong = img_bytes[0:1024]
print(len(img_bytes))