from icrawler.builtin import GoogleImageCrawler
import sys
import os

SAVE_DIR = "files/"

argv = sys.argv

if not os.path.isdir(argv[1]):
    os.makedirs(SAVE_DIR + argv[1])

crawler = GoogleImageCrawler(storage = {"root_dir": SAVE_DIR + argv[1]})
crawler.crawl(keyword = argv[1], max_num = int(argv[2]))
