import base64

import cv2
import numpy as np
from flask import render_template, request

from colorapp import app
from colorapp.utils.response import FormResponse
from colorapp.utils.image import create_n_img
from colorapp.utils.image import resize_image
from colorapp.utils.image import remove_background
from colorapp.utils.color import get_color_pallet
from colorapp.utils.color import get_nearest_color
from colorapp.utils.color import rgb2hex


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # ブラウザによるアクセス制御
        return render_template('colorapp/index.html')
    elif request.method == 'POST':
        # 画像処理
        file = request.files['image_file']
        stream = file.stream
        img_raw = np.asarray(bytearray(stream.read()), dtype=np.uint8)
        image = cv2.imdecode(img_raw, cv2.IMREAD_UNCHANGED)
        # フォームのリスポンスを整形したオブジェクトを生成
        fr = FormResponse(response=request.form)
        if fr.need_resize():
            image = resize_image(image)
        if fr.need_rembg():
            image = remove_background(image)
        dtype = image.dtype
        # カラーパレットの生成
        n_img = create_n_img(image, fr.need_rembg())
        color_pallet, rgb = get_color_pallet(n_img=n_img, n_clusters=fr.get_n_clusters(), dtype=dtype)

        if fr.request_base_color():
            # ベースカラー
            return render_template('colorapp/basecolor.html', result=__on_request_base_color(fr, color_pallet, rgb))
        elif fr.request_nearest_base_color():
            # ニアレストカラー
            return render_template('colorapp/nearestcolor.html', result=__on_request_nearest_base_color(fr, color_pallet, rgb))
        else:
            # カラーパレット
            return render_template('colorapp/colorpallet.html', result=__on_request_color_pallet(fr, color_pallet, rgb))


@app.route('/api', methods=['POST'])
def api():
    if 'image' not in request.form:
        return None
    base64_image = request.form['image']
    img_raw = base64.b64decode(base64_image)
    nparr = np.frombuffer(img_raw, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
    # フォームのリスポンスを整形したオブジェクトを生成
    fr = FormResponse(response=request.form)
    if fr.need_resize():
        image = resize_image(image)
    if fr.need_rembg():
        image = remove_background(image)
    dtype = image.dtype
    # カラーパレットの生成
    n_img = create_n_img(image, fr.need_rembg())
    color_pallet, rgb = get_color_pallet(n_img=n_img, n_clusters=fr.get_n_clusters(), dtype=dtype)

    if fr.request_base_color():
        # ベースカラー
        return __on_request_base_color(fr, color_pallet, rgb)
    elif fr.request_nearest_base_color():
        # ニアレストカラー
        return __on_request_nearest_base_color(fr, color_pallet, rgb)
    else:
        # カラーパレット
        return __on_request_color_pallet(fr, color_pallet, rgb)


def __on_request_base_color(response, color_pallet, rgb):
    base_color_hex = color_pallet[0][0]
    base_color_rgb = rgb[base_color_hex]
    return {'hex': base_color_hex, 'rgb': base_color_rgb}


def __on_request_nearest_base_color(response, color_pallet, rgb):
    base_pallet = response.get_base_pallet()
    base_color_hex = color_pallet[0][0]
    base_color_rgb = rgb[base_color_hex]
    nearest_color_rgb, nearest_color_name = get_nearest_color(base_color_rgb, base_pallet)
    nearest_color_hex = rgb2hex(*nearest_color_rgb)
    return {'base': {'hex': base_color_hex, 'rgb': base_color_rgb},
            'nearest': {'name': nearest_color_name, 'hex': nearest_color_hex, 'rgb': nearest_color_rgb}}


def __on_request_color_pallet(response, color_pallet, rgb):
    return {'color_pallet': color_pallet, 'rgb': rgb}
