import cv2
import numpy as np
from rembg import remove


def create_n_img(image, has_alpha=True):
    """画像をリシェイプし、必要に応じてアルファチャンネルを考慮してフィルタリングする関数

    Args:
        image: 入力画像
        has_alpha: アルファチャンネルがあるかどうか（デフォルトはTrue）

    Returns:
        リシェイプされた画像データのnumpy配列
    """
    if has_alpha:
        img = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
        reshaped_img = np.reshape(img, (img.shape[0] * img.shape[1], 4))
        return np.array(list(filter(lambda nim: nim[3] > 0, reshaped_img)))
    else:
        img = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
        return np.reshape(img, (img.shape[0] * img.shape[1], 3))


def resize_image(image, max_size=1000):
    """画像を指定された最大サイズにリサイズする関数

    Args:
        image: 入力画像
        max_size: 最大サイズ（デフォルトは1000）

    Returns:
        リサイズされた画像
    """
    width, height = image.shape[:2]
    if max(width, height) <= max_size:
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
    """画像の背景を削除する関数

    Args:
        image: 入力画像

    Returns:
        背景が削除された画像
    """
    return remove(image)

