from flask import Flask, render_template, request, redirect, send_from_directory
import cv2
from datetime import datetime
import os
import string
import random
import tensorflow as tf
from keras.models import model_from_json
from keras.preprocessing import image
import numpy as np

# 保存したモデルの読み込み
model = model_from_json(open('../data/my_predict.json').read())
# 保存した重みの読み込み
model.load_weights('../data/my_predict.hdf5')
graph = tf.get_default_graph()

SAVE_DIR = "images/"
if not os.path.isdir(SAVE_DIR):
    os.mkdir(SAVE_DIR)

app = Flask(__name__, static_url_path="")


def random_str(n):
    return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(n)])


@app.route('/')
def index():
    # 隠しファイルを除いたファイルリストを取得
    file_list = [filename for filename in os.listdir(SAVE_DIR) if not filename.startswith('.')]
    return render_template('index.html', images=file_list)


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
        dt_now = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        save_path = os.path.join(SAVE_DIR, dt_now + ".png")
        cv2.imwrite(save_path, img)
        print("save", save_path)

        # 判定
        # 画像を読み込む
        img = image.load_img(SAVE_DIR + "/" + dt_now + ".png", target_size=(256, 256, 3))
        x = image.img_to_array(img)
        print(x)
        x = np.expand_dims(x, axis=0)

        # 予測
        global graph
        with graph.as_default():
            features = model.predict(x)

        # 予測結果によって処理を分ける
        if features[0, 0] == 1:
            category = "醤油ラーメン"
        elif features[0, 1] == 1:
            category = "味噌ラーメン"
        elif features[0, 2] == 1:
            category = "担々麺"
        else:
            category = "unknown"
        os.rename(SAVE_DIR + dt_now + ".png", SAVE_DIR + "/" + dt_now + "_" + category + ".png")

        return redirect('/')


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=8080)
