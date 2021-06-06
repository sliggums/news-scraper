from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join, TakeFirst, Compose, TakeFirst
from newsscraper.items import NewsItem
from scrapy.spiders import CrawlSpider, Rule

BANNED_PREFIXES = set(['Uploaded:', 'Updated:', 'and', 'for', 'Email'])

def filter_text(item):
  if len(item) < 10:
    return ''
  split = item.split()
  return item if len(split) and (split[0] not in BANNED_PREFIXES) and item[0] is not '\n' else ''

class DanvilleSanRamonLoader(ItemLoader):
  title_in = MapCompose(str.strip)
  title_out = TakeFirst()

  title_hash_in = MapCompose(hash)
  title_hash_out = TakeFirst()

  text_in = MapCompose(filter_text, str.strip)
  text_out = Join(" ")

class QuotesSpider(CrawlSpider):
  CLOSESPIDER_ITEMCOUNT = 1
  name = "danvillesanramon"
  start_urls = ['https://www.danvillesanramon.com/news/recent_headlines.php']

  # TODO: /news/ or /blogs/
  rules = (
    Rule(LinkExtractor(restrict_xpaths=r'//a[starts-with(@href, "/news/")]'), callback='parse_item'),
  )

  def parse_item(self, response):
    loader = DanvilleSanRamonLoader(item=NewsItem(), response=response)
    loader.add_xpath('title', '//h1/text()')
    loader.add_xpath('title_hash', '//h1/text()')
    loader.add_xpath('text', '//div[@class="text-block"]/p/text()')
    yield loader.load_item()