# ml_sample_project
## install
```
pip install icrawler
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
