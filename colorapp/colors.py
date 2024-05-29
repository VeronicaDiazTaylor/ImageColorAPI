import colorsys
import cv2
import numpy as np
from rembg import remove
import matplotlib.colors as cs
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


JIS_COLOR_PENCIL = {
    "薄紅色": (197, 103, 112),
    "紅色": (187, 62, 83),
    "赤色": (194, 56, 63),
    "紅樺色": (128, 65, 61),
    "朱色": (224, 86, 69),
    "赤茶色": (173, 78, 57),
    "茶色": (124, 86, 66),
    "焦茶色": (87, 69, 58),
    "橙色": (255, 137, 68),
    "蜜柑色": (252, 166, 59),
    "土色": (159, 108, 49),
    "黄土色": (185, 135, 68),
    "朽葉色": (132, 116, 97),
    "山吹色": (251, 189, 45),
    "卵色": (251, 226, 139),
    "黄色": (243, 212, 37),
    "檸檬色": (242, 231, 96),
    "黄緑色": (148, 166, 57),
    "松葉色": (69, 119, 49),
    "灰緑色": (81, 101, 60),
    "緑色": (0, 137, 84),
    "若竹色": (58, 177, 120),
    "深緑色": (35, 93, 80),
    "常盤色": (44, 106, 75),
    "青磁色": (128, 165, 143),
    "薄青緑色": (49, 157, 166),
    "青緑色": (0, 106, 104),
    "納戸色": (0, 94, 108),
    "水色": (94, 165, 196),
    "薄青色": (106, 160, 213),
    "青色": (67, 107, 161),
    "藍色": (36, 73, 116),
    "薄群青色": (94, 131, 188),
    "群青色": (0, 83, 148),
    "藤色": (162, 147, 204),
    "藤紫色": (123, 110, 162),
    "菫色": (106, 65, 131),
    "薄紫色": (157, 117, 156),
    "紫色": (74, 63, 117),
    "赤紫色": (148, 68, 94),
    "濃赤紫色": (100, 60, 81),
    "桃色": (216, 130, 165),
    "白色": (225, 226, 226),
    "鼠色": (143, 143, 143),
    "灰色": (118, 118, 118),
    "黒色": (0, 0, 0),
}


def __rgb2hsv(rgb):
    r, g, b = rgb
    return colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)


def get_closest_color(rgb: tuple[int, int, int], base_pallet=JIS_COLOR_PENCIL):
    base_hsv = __rgb2hsv(rgb)
    dh = 0
    ds = 0
    dv = 0
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
        colors.append(tuple(clt.cluster_centers_[i] / 255))
        hex_ = cs.to_hex(tuple(clt.cluster_centers_[i] / 255))
        hex_labels.append(hex_)
        rgb[hex_] = hex2rgb(hex_)
    dc = dict(zip(hex_labels, hist))
    dc_sorted = sorted(dc.items(), key=lambda x: x[1], reverse=True)
    return dc_sorted, rgb


def get_nearest_color(image):
    pass
