# -*- coding: utf-8 -*-
import scrapy

class BadboySpider(scrapy.Spider):
    name = 'badboy'
    allowed_domains = ['badboymowers.com']
    start_urls = ['https://www.badboymowers.com/bad-boy-shop/zero-turn-mowers']

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse,)

    def parse(self, response):
        product_container = response.css('div.content-wrap div.orange-bg div.row div.footer-commercial')
        # product_cat = product_container.css('h4.angled-heading::text').get()
        for products in product_container.css('div.flex-fill'):
            product_url = products.css("a::attr(href)").get()
            product_url = 'https://www.badboymowers.com'+product_url
            yield {
                'category': "Professional-Grade Commercial Zero-Turn Mowers",
                'url': product_url,
            }
