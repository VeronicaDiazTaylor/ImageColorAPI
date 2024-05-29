import cv2
import numpy as np
from rembg import remove


def create_n_img(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
    reshaped_img = np.reshape(img, (img.shape[0] * img.shape[1], 4))
    return np.array(list(filter(lambda nim: nim[3] > 0, reshaped_img)))


def resize_image(image, max_size=1000):
    width, height = image.shape[:2]
    if width > max_size and height > max_size:
        return image
    aspect_ratio = width / height
    if width > height:
        new_width = max_size
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = max_size
        new_width = int(new_height * aspect_ratio)
    return cv2.resize(image, (new_width, new_height))


def remove_background(image):
    return remove(image)

