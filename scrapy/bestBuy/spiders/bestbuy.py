import json
import time
import re
import sys
import scrapy


class BestBuySpider(scrapy.Spider):
    name = "products"
    front_url = "https://www.bestbuy.com/site/searchpage.jsp?cp="
    middle_url = "&searchType=search&st="
    end_url = "&_dyncharset=UTF-8&id=pcat17071&type=page&sc=Global&nrp=&sp=&qp=&list=n&af=true&iht=y&intl=nosplash&usc=All%20Categories&ks=960&keys=keys"

    def start_requests(self):
        keywords = self.get_keywords()

        for k in keywords:
            yield scrapy.Request(url=self.front_url + "1" + self.middle_url + k.name + self.end_url, callback=self.parse,
                                 meta={'category': k.category, 'subcategory': k.sub_category, 'search_term': k.name })

    def parse(self, response):
        for product in response.css('li.sku-item'):
            new_product_indicator = product.css("span.new-indicator::text").get()
            product_name = product.css("h4.sku-header > a::text").get()
            product_url = product.css("h4.sku-header >  a::attr(href)").get()
            if product_url is not None:
                product_url = 'https://www.bestbuy.com' + str(product_url)
            else:
                product_url = 'url not found'
            if new_product_indicator:
                rating = '0'
                reviews = 'New Product'
            else:
                rating = product.css("div.ugc-ratings-reviews > i::attr(alt)").get()
                if rating is not None:
                    if float(rating) > 0:
                        reviews = product.css('span.c-total-reviews::text').extract()[1]
                    else:
                        reviews = product.css('span.c-reviews-none::text').get()
                else:
                    reviews = product.css('span.c-reviews-none::text').get()

            yield {
                'product_name': product_name,
                'searchTerm': response.meta.get('search_term'),
                'category': response.meta.get('category'),
                'sub_category': response.meta.get('subcategory'),
                'rating': rating,
                'reviews': reviews,
                'url': product_url,
            }
        next_page = response.css('div.right-side a.ficon-caret-right::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def get_keywords(self):
        keywords = []
        with open('input.json', encoding="utf8") as jsonFile:
            json_data = json.load(jsonFile)
            for data in json_data:
                search_name = data['name']
                cat = data['category']
                sub_cat = data['subcategory']
                try:
                    if search_name is not None:
                        if search_name.lower != 'none':
                            keywords.append(Keyword(search_name, cat, sub_cat))
                except Exception as e:
                    print(e)
                    print("Oops!", sys.exc_info()[0], "occured.")
                    pass
        return keywords


class Keyword:
    def __init__(self, name, category, sub_category):
        self.name = name
        self.category = category
        self.sub_category = sub_category
