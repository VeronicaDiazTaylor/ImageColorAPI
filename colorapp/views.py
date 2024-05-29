import cv2
import numpy as np
from flask import render_template, request

from colorapp import app
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
        # フォームのリザルトを格納
        response = request.form
        # 画像処理
        file = request.files['image_file']
        stream = file.stream
        img_raw = np.asarray(bytearray(stream.read()), dtype=np.uint8)
        image = cv2.imdecode(img_raw, cv2.IMREAD_UNCHANGED)
        image = resize_image(image)
        if 'remove_background' in response:
            image = remove_background(image)
        # カラーパレットの生成
        n_clusters = 5
        if 'n_clusters' in response:
            n_clusters = int(response['n_clusters'])
        color_pallet, rgb = get_color_pallet(create_n_img(image), n_clusters=n_clusters)
        process = response['process']

        if process == 'base-color':
            # ベースカラー
            base_color_hex = color_pallet[0][0]
            base_color_rgb = rgb[base_color_hex]
            result = {'hex': base_color_hex, 'rgb': base_color_rgb}
            return render_template('colorapp/basecolor.html', result=result)
        elif process == 'nearest-base-color':
            # ニアレストカラー
            base_pallet = response['base_pallet']
            base_color_hex = color_pallet[0][0]
            base_color_rgb = rgb[base_color_hex]
            nearest_color_rgb, nearest_color_name = get_nearest_color(base_color_rgb, base_pallet)
            nearest_color_hex = rgb2hex(*nearest_color_rgb)
            result = {'base': {'hex': base_color_hex, 'rgb': base_color_rgb},
                      'nearest': {'name': nearest_color_name, 'hex': nearest_color_hex, 'rgb': nearest_color_rgb}}
            return render_template('colorapp/nearestcolor.html', result=result)
        else:
            # カラーパレット
            result = {'color_pallet': color_pallet, 'rgb': rgb}
            return render_template('colorapp/colorpallet.html', result=result)
