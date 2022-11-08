import scrapy
from scrapy.http import HtmlResponse
import json
from datetime import datetime


class GlobusSpider(scrapy.Spider):
    name = 'globus'
    allowed_domains = ['globus-online.kg']
    start_urls = ['https://globus-online.kg/catalog/']
    URL = 'https://globus-online.kg/catalog'

    def parse(self, response):
        category_urls = response.xpath('//li[contains(@class, "section")]/a/@href').getall()

        for url in category_urls:
            url = 'https://globus-online.kg' + url + '?ajaxpages=Y&ajaxpagesid=ajaxpages_gmci&PAGEN_1=1'
            yield scrapy.Request(
                    url=url,
                    callback=self.parse_category,
                    # dont_filter=True,
                    )

    def parse_category(self, response):
        data = json.loads(response.body)
        html = data['HTMLBYCLASS']['view-showcase']
        html_response = HtmlResponse(
                url=response.url,
                body=html,
                encoding='utf-8',
                )
        items = html_response.xpath('//div[contains(@class, "js-autoscroll-item list-element list-showcase__element")]')

        ajaxpages = data['HTML']['catalogajaxpages']
        if ajaxpages != '':

            for item in items:
                item_name = item.xpath('.//div[@class="list-showcase__name"]/a/text()').get()
                url = item.xpath('.//div[@class="list-showcase__name"]/a/@href').get()
                price = item.xpath('.//span[contains(@class, "c-prices__price")]/@data-price').get()
                image = item.xpath('.//div[@class="list-showcase__picture"]/a/img/@data-src').get()
                if url is not None:
                    url = 'https://globus-online.kg' + url
                if image is not None:
                    image = self.URL + image


                yield {
                        'shop_name': self.name,
                        'item_name': item_name,
                        'price': price,
                        'image': image,
                        'url': url,
                        'parse_datetime': datetime.now(),
                        }

            html_ajaxpages = HtmlResponse(url=response.url, body=data['HTML']['catalogajaxpages'], encoding='utf-8')
            current_page = int(html_ajaxpages.xpath('//a/@data-navpagenomer').get())
            next_page = response.url[:response.url.rfind('=')] + f'={current_page + 1}'
            
            # yield response.follow(
            #         next_page,
            #         callback=self.parse_category,
            #         )

            yield scrapy.Request(
                    url=next_page,
                    callback=self.parse_category,
                    )
