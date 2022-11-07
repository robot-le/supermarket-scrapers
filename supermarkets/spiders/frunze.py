import scrapy
from datetime import datetime


class FrunzeSpider(scrapy.Spider):
    name = 'frunze'
    allowed_domains = ['online.gipermarket.kg']
    start_urls = ['https://online.gipermarket.kg/catalog/']

    def parse(self, response):
        category_urls = response.xpath('//div[@class="item columns"]/div/div[2]/a/@href').getall()

        for url in category_urls:
            yield scrapy.Request(
                    url='https://online.gipermarket.kg' + url + '?PAGE_EL_COUNT=64&PAGEN_1=1',
                    # url='https://online.gipermarket.kg' + url + '?PAGEN_1=1',
                    callback=self.parse_category,
                    )


    def parse_category(self, response):

        item_elements = response.xpath('//div[@class="product-list-item table-container h100pc"]')

        for item in item_elements:

            url = 'https://online.gipermarket.kg' + item.xpath('.//a[@class="name"]/@href').get()
            image = item.xpath('.//img[@class="thumbnail"]/@src').get()
            item_name = item.xpath('.//a[@class="name"]/text()').get()
            price = int(item.xpath('.//div[@class="price"]/text()').get().replace('сом', '').replace(' ', ''))

            yield {
                    'shop_name': self.name,
                    'item_name': item_name,
                    'price': price,
                    'image': 'https://online.gipermarket.kg' + image,
                    'url': url,
                    'parse_datetime': datetime.now(),
                    }

        pages = response.xpath('//div[@class="catalog-pagination"]/a/text()').getall()
        max_page = sorted([int(x) for x in pages if x.isdigit()])[-1]
        current_page = int(response.url[response.url.rfind('=') + 1:])
        next_page = response.url[:response.url.rfind('=')] + f'={current_page + 1}'

        if current_page + 1 <= max_page:
            yield response.follow(
                    next_page,
                    callback=self.parse_category,
                    )
        
