import scrapy


class FrunzeSpider(scrapy.Spider):
    name = 'frunze'
    allowed_domains = ['online.gipermarket.kg']
    start_urls = ['http://online.gipermarket.kg/']

    def parse(self, response):
        pass
