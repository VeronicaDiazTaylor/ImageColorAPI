import colorsys

import matplotlib.colors as cs
import numpy as np
from sklearn.cluster import KMeans

from colorapp.utils.pallet import PALLET


def hex2rgb(hex_value) -> tuple[int, int, int]:
    hex_code = hex_value.lstrip("#")
    rgb_code = [int(hex_code[i:i + 2], 16) for i in range(0, 6, 2)]
    return rgb_code[0], rgb_code[1], rgb_code[2]


def rgb2hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def rgb2hsv(rgb):
    r, g, b = rgb
    return colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)


def get_color_pallet(n_img, n_clusters=5, dtype=np.uint8):
    clt = KMeans(n_clusters=n_clusters)
    clt.fit(n_img)
    labels = np.unique(clt.labels_)
    hist, _ = np.histogram(clt.labels_, bins=np.arange(len(labels) + 1))
    hex_labels = []
    rgb = {}
    all_alpha = []
    divide = np.iinfo(dtype).max - 1
    for i in range(clt.cluster_centers_.shape[0]):
        hex_ = cs.to_hex(tuple(clt.cluster_centers_[i] / divide))
        hex_labels.append(hex_)
        rgb[hex_] = hex2rgb(hex_)
    dc = dict(zip(hex_labels, hist))
    dc_sorted = sorted(dc.items(), key=lambda x: x[1], reverse=True)
    return dc_sorted, rgb


def get_nearest_color(rgb: tuple[int, int, int], pallet_identifier='j'):
    base_pallet = PALLET[pallet_identifier]
    base_hsv = rgb2hsv(rgb)
    tolerance_h = 0.01
    tolerance_s = 0.01
    tolerance_v = 0.8
    color_entry = {}
    for nm, pallet in base_pallet.items():
        target_hsv = rgb2hsv(pallet)
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
