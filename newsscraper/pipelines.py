
# -*- coding: utf-8 -*-
from csv import DictWriter
from newsscraper.items import NewsItem
from datetime import date

BANNED_TITLES = set(['Stay informed.'])

class NewsscraperPipeline:

	def open_spider(self, spider):
		datestring = date.today().strftime("%m%d%y")
		path = datestring + spider.name + ".csv"
		self.file = open(path, 'a+')
		self.csvwriter = DictWriter(self.file, 
			fieldnames=list(NewsItem.fields.keys()))

	def close_spider(self, spider):
		self.file.close()

	def process_item(self, item, spider):
		if 'title' in item and item['title'] not in BANNED_TITLES:
			self.csvwriter.writerow(dict(item))
			return item
