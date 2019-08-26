from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import numpy as np
import cv2
# from image_process import ramen
from datetime import datetime
import os
import string
import random
import tensorflow as tf
from keras import models
from keras.models import model_from_json
from keras.preprocessing import image
import numpy as np

#保存したモデルの読み込み
model = model_from_json(open('./data/ramen_predict.json').read())
#保存した重みの読み込み
model.load_weights('./data/ramen_predict.hdf5')
graph = tf.get_default_graph()

# ラーメンの分類
categories = ["醤油ラーメン","味噌ラーメン","塩ラーメン","豚骨ラーメン","担々麺"]

SAVE_DIR = "./images"
if not os.path.isdir(SAVE_DIR):
    os.mkdir(SAVE_DIR)

app = Flask(__name__, static_url_path="")

def random_str(n):
    return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(n)])

@app.route('/')
def index():
    return render_template('index.html', images=os.listdir(SAVE_DIR)[::-1])

@app.route('/images/<path:path>')
def send_js(path):
    return send_from_directory(SAVE_DIR, path)

# 参考: https://qiita.com/yuuuu3/items/6e4206fdc8c83747544b
@app.route('/upload', methods=['POST'])
def upload():
    if request.files['image']:
        # 画像として読み込み
        stream = request.files['image'].stream
        img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
        img = cv2.imdecode(img_array, 1)

        # 保存
        dt_now = datetime.now().strftime("%Y_%m_%d%_H_%M_%S_")
        save_path = os.path.join(SAVE_DIR, dt_now + ".png")
        cv2.imwrite(save_path, img)
        print("save", save_path)

        # 変換
        # img = canny(img)

        # 判定
        #画像を読み込む
        img = image.load_img(SAVE_DIR + "/" + dt_now + ".png", target_size=(256, 256, 3))
        x = image.img_to_array(img)
        print(x)
        x = np.expand_dims(x, axis=0)

        #予測
        global graph
        with graph.as_default():
            features = model.predict(x)

        #予測結果によって処理を分ける
        ramen_type = ""
        if features[0,0] == 1:
            ramen_type = "醤油ラーメン"
        elif features[0,1] == 1:
            ramen_type = "味噌ラーメン"
        elif features[0,2] == 1:
            ramen_type = "塩ラーメン"
        elif features[0,3] == 1:
            ramen_type = "豚骨ラーメン"
        elif features[0,4] == 1:
            ramen_type = "担々麺"
        else:
            ramen_type = "unknown"
        os.rename(SAVE_DIR + "/" + dt_now + ".png", SAVE_DIR + "/" + dt_now + "_" + ramen_type + ".png")

        return redirect('/')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8888)
