import scrapy


class GlobusSpider(scrapy.Spider):
    name = 'globus'
    allowed_domains = ['globus-online.kg']
    start_urls = ['http://globus-online.kg/']

    def parse(self, response):
        pass
