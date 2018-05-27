import scrapy
import math


URL_TMPL = "http://www.focus-news.net/news/2017/07/24/{}"

FIRST_ARTICLE = 2457151
LAST_ARTICLE = FIRST_ARTICLE + 10000
DELAY = 0.5

class FocusNewsSpider(scrapy.Spider):
  name = "focusnews"
  download_delay = DELAY
  custom_settings = {
      'FEED_EXPORT_ENCODING': 'utf-8'
  }

  def __init__(self, first_article=FIRST_ARTICLE, last_article=LAST_ARTICLE):
    self.start_urls = [URL_TMPL.format(x)
        for x in range(int(first_article), int(last_article))]

  def parse(self, response):
    title = response.css('.inside-top-title h1::text').extract_first()
    body = response.css(".print-content .inside-body-content").extract_first()

    yield {
      'title': title,
      'body': body
    }
