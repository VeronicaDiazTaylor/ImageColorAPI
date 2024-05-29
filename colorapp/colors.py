import colorsys
import cv2
import numpy as np
from rembg import remove
import matplotlib.colors as cs
from sklearn.cluster import KMeans

from colorapp.base_pallet import JIS_COLOR_PENCIL
from colorapp.base_pallet import BASE_COLOR_140
from colorapp.base_pallet import JAPANESE_COLOR_465


def __rgb2hsv(rgb):
    r, g, b = rgb
    return colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)


def get_closest_color(rgb: tuple[int, int, int], pallet='j'):
    if pallet == 'd':
        base_pallet = BASE_COLOR_140
    elif pallet == 'w':
        base_pallet = JAPANESE_COLOR_465
    else:
        base_pallet = JIS_COLOR_PENCIL
    base_hsv = __rgb2hsv(rgb)
    tolerance_h = 0.1
    tolerance_s = 0.1
    tolerance_v = 1
    color_entry = {}
    for nm, pallet in base_pallet.items():
        target_hsv = __rgb2hsv(pallet)
        hue_diff = abs(base_hsv[0] - target_hsv[0])
        saturation_diff = abs(base_hsv[1] - target_hsv[1])
        value_diff = abs(base_hsv[2] - target_hsv[2])
        if hue_diff < tolerance_h and saturation_diff < tolerance_s and value_diff < tolerance_v:
            color_entry[nm] = pallet
    if len(color_entry) == 0:
        color_entry = base_pallet
    closest = None
    min_distance = float('inf')
    for name, color in color_entry.items():
        distance = sum((a - b) ** 2 for a, b in zip(rgb, color))
        if distance < min_distance:
            min_distance = distance
            closest = name
    return base_pallet[closest], closest


def hex2rgb(hex_value) -> tuple[int, int, int]:
    hex_code = hex_value.lstrip("#")
    rgb_code = [int(hex_code[i:i+2], 16) for i in range(0, 6, 2)]
    return rgb_code[0], rgb_code[1], rgb_code[2]


def rgb2hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def get_base_color(image):
    pass


def get_color_pallet(image_raw, need_rembg):
    image = cv2.imdecode(image_raw, cv2.IMREAD_UNCHANGED)
    width, height = image.shape[:2]
    aspect_ratio = width / height
    if width > height:
        new_width = 800
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = 800
        new_width = int(new_height * aspect_ratio)
    image = cv2.resize(image, (new_width, new_height))
    if need_rembg:
        image = remove(image)
    img = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
    reshaped_img = np.reshape(img, (img.shape[0] * img.shape[1], 4))
    n_img = np.array(list(filter(lambda nim: nim[3] > 0, reshaped_img)))
    clt = KMeans(n_clusters=5)
    clt.fit(n_img)
    labels = np.unique(clt.labels_)
    hist, _ = np.histogram(clt.labels_, bins=np.arange(len(labels) + 1))
    colors = []
    hex_labels = []
    rgb = {}
    for i in range(clt.cluster_centers_.shape[0]):
        print(tuple(clt.cluster_centers_[i] / 255))
        colors.append(tuple(clt.cluster_centers_[i] / 255))
        hex_ = cs.to_hex(tuple(clt.cluster_centers_[i] / 255))
        hex_labels.append(hex_)
        rgb[hex_] = hex2rgb(hex_)
    dc = dict(zip(hex_labels, hist))
    dc_sorted = sorted(dc.items(), key=lambda x: x[1], reverse=True)
    return dc_sorted, rgb
