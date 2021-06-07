from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join, TakeFirst, Compose, TakeFirst
from newsscraper.items import NewsItem
from scrapy.spiders import CrawlSpider, Rule
from w3lib.html import remove_tags

class VergeLoader(ItemLoader):
  title_in = MapCompose(str.strip)
  title_out = TakeFirst()

  title_hash_in = MapCompose(hash)
  title_hash_out = TakeFirst()

  text_in = MapCompose(str.strip, remove_tags)
  text_out = Join(" ")

class VergeSpider(CrawlSpider):
  name = "verge"
  start_urls = ['https://www.theverge.com']

  rules = (
    Rule(LinkExtractor(restrict_xpaths=r'//a[starts-with(@href, \
      "https://www.theverge.com/202")]'), callback='parse_item'),
  )

  def parse_item(self, response):
    loader = VergeLoader(item=NewsItem(), response=response)
    loader.add_xpath('title', '//h1[@class="c-page-title"]/text()')
    loader.add_xpath('title_hash', '//h1[@class="c-page-title"]/text()')
    loader.add_xpath('text', '//div[@class="c-entry-content "]/p')
    yield loader.load_item()