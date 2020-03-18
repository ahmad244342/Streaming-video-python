import numpy as np

class flip_img:
    def __init__(self, img):
        self.img = img
        self.img_array = np.array(img)

    def start(self):
        img_save = list(map(lambda data_array: np.flipud(data_array), self.img_array))
        return np.array(img_save)
