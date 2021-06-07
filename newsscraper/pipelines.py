
# -*- coding: utf-8 -*-
from csv import DictWriter
from newsscraper.items import NewsItem

WRITE_PATH = 'test.csv'

BANNED_TITLES = set(['Stay informed.'])

class NewsscraperPipeline:

    def open_spider(self, spider):
        self.file = open(WRITE_PATH, 'a+')
        self.csvwriter = DictWriter(self.file, 
            fieldnames=list(NewsItem.fields.keys()))

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if 'title' in item and item['title'] not in BANNED_TITLES:
            self.csvwriter.writerow(dict(item))
            return item
