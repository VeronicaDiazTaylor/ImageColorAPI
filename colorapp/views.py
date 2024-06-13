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
            base_color_hex = color_pallet[0][0]
            base_color_rgb = rgb[base_color_hex]
            result = {'hex': base_color_hex, 'rgb': base_color_rgb}
            return render_template('colorapp/basecolor.html', result=result)
        elif fr.request_nearest_base_color():
            # ニアレストカラー
            base_pallet = fr.get_base_pallet()
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
