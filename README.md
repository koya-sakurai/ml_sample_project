# ml_sample_project
## install
```
pip install icrawler, flask, keras, opencv-python, Pillow
```
## How to use
1. 学習・検証データとなる画像ファイルを収集する
```
cd image/
python image_collector.py [検索ワード] [取得画像数]
# e.g. python image_collector.py 味噌ラーメン 100
```
2. Jupyter Notebookを起動し、my_project.ipynbを開く
```
cd ../
sh jupyter_notebook.sh
```
3. my_project.ipynbの内容を自分のテーマに合わせて編集し実行する
4. 学習結果の確認用Webサービスを起動する
```
python web/server.py
```
5. 確認用Webサービスで画像を読み込ませて結果を確認する
