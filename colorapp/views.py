import os
import base64

import numpy as np
from flask import render_template, request, redirect, url_for, jsonify
from colorapp import app
import colorapp.colors as colors


def __error(message, replace=[]):
    for i in range(len(replace)):
        message = message.replace('{%' + i + '}', replace[i])
    return message, 400


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('colorapp/index.html')
    elif request.method == 'POST':
        response = request.form
        file = request.files['image_file']
        image_name = file.filename
        stream = file.stream
        img_raw = np.asarray(bytearray(stream.read()), dtype=np.uint8)
        process = response['process']
        need_rembg = 'remove_background' in response
        color_pallet, rgb = colors.get_color_pallet(img_raw, need_rembg)

        if process == 'base-color':
            base_color_hex = color_pallet[0][0]
            base_color_rgb = rgb[base_color_hex]
            result = {
                'hex': base_color_hex,
                'rgb': base_color_rgb
            }
            return render_template('colorapp/basecolor.html', result=result)
        elif process == 'nearest-base-color':
            base_color_hex = color_pallet[0][0]
            base_color_rgb = rgb[base_color_hex]
            base_color_hex = colors.rgb2hex(*base_color_rgb)
            nearest_color_rgb, nearest_color_name = colors.get_closest_color(base_color_rgb)
            nearest_color_hex = colors.rgb2hex(*nearest_color_rgb)
            result = {
                'base': {
                    'hex': base_color_hex,
                    'rgb': base_color_rgb
                },
                'nearest': {
                    'name': nearest_color_name,
                    'hex': nearest_color_hex,
                    'rgb': nearest_color_rgb
                }
            }
            return render_template('colorapp/nearestcolor.html', result=result)
        else:
            result = {
                'color_pallet': color_pallet,
                'rgb': rgb
            }
            return render_template('colorapp/colorpallet.html', result=result)
