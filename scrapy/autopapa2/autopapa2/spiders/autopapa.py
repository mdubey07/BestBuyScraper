from pyexcel.cookbook import merge_all_to_a_book
import os
import csv
import glob
from openpyxl import Workbook
from scrapy import signals
import scrapy
from ..helpers.autopapa_helper import AutopapaHelper
from ..helpers.item_helper import ItemHelper


class AutopapaSpider(scrapy.Spider, AutopapaHelper, ItemHelper):
    name = 'autopapa'

    start_urls = [
        'https://autopapa.ge/ge/search?utf8=%E2%9C%93&short_form=0&s%5Bbrand_id%5D=0&s%5Byear_from%5D=0&s%5Bprice_from%5D=&s%5Bcountry_id%5D=2&s%5Bengine_type%5D%5B%5D=0&s%5Blegal_status%5D%5B%5D=&s%5Brudder%5D%5B%5D=&s%5Bmodel_id%5D=0&s%5Byear_to%5D=0&s%5Bprice_to%5D=&s%5Bcity_id%5D=0&s%5Bgearbox%5D%5B%5D=0'
    ]

    url = 'https://autopapa.ge/ge/search?&s%5Bcountry_id%5D=2&order=date&page={}&short_form=0&utf8=%E2%9C%93'

    allowed_domains = [
        'autopapa.ge'
    ]

    def parse(self, response):
        number_of_pages = response.xpath('//*[@class="pageNumber"]//text()').extract()[-1]
        number_of_pages = int(number_of_pages)
        number_of_pages = 2

        for page in range(1, number_of_pages + 1):
            url = self.url.format(page, )
            yield scrapy.Request(url, self.parse_pages)

    def parse_pages(self, response):
        cars = response.xpath('//*[@class="flag-box"]//@href').extract()
        for car in cars:
            car_url = f'https://autopapa.ge{car}'
            yield scrapy.Request(car_url, self.parse_car)

    def parse_car(self, response):

        self.helper_response = response

        item = self.make_item(
            production_year=self.get_production_year(),
            nav_list='|'.join(self.get_nav_list()),
            unique_name=self.get_unique_name(),
            nav_make=self.nav_list_items(self.get_nav_list())['make'],
            nav_series=self.nav_list_items(self.get_nav_list())['series'],
            nav_modal=self.nav_list_items(self.get_nav_list())['modal'],
            gear_box=self.car_add_pair_info(self.car_add_infos(self.get_car_description())[0], 'გადაცემათა კოლოფი'),
            steering_wheel=self.car_add_pair_info(self.car_add_infos(self.get_car_description())[0], 'საჭე'),
            condition=self.get_condition(),
            engine_type=self.get_engine_type(),
            power=self.get_power(),
            engine_volume=self.get_engine_volume(),
            mileage=self.get_mileage(),
            drive_wheels=self.get_drive_wheels(),
            doors=self.get_doors(),
            number_of_seats=self.get_number_of_seats(),
            color=self.get_color(),
            model=self.get_model(),
            price=self.get_price(),
            # price_currency=self.get_price_currency(),
            name=self.get_name(),
            customs=self.get_customs(),
            seller_phone=self.get_seller_phone(),
            car_description=self.get_car_description(),
            seller_comment=self.get_seller_comment(),
            seller=self.get_seller(),
            location=self.get_location(),
            body_type=self.get_body_type(),
            # images=self.get_images(),
            image_urls=self.get_images()
        )

        yield item

    @staticmethod
    def nav_list_items(list_items):
        car_info = {
            'make': '',
            'series': '',
            'modal': ''
        }
        if list_items:
            if len(list_items) == 3:
                car_info['make'] = list_items[0]
                car_info['series'] = list_items[1]
                car_info['modal'] = list_items[2]
            else:
                car_info['make'] = list_items[0]
                car_info['series'] = 'NA'
                car_info['modal'] = list_items[1]
        return car_info

    @staticmethod
    def car_add_infos(item_str):
        pair_list = []
        un_pair_list = []
        combine_list = []

        for s in item_str.split(','):
            if ':' in s:
                pair_list.append(s.strip())
            else:
                un_pair_list.append(s.strip())
        combine_list.append(pair_list)
        combine_list.append(un_pair_list)
        return combine_list

    @staticmethod
    def car_add_pair_info(item_list, search_term):
        add_info = {}
        for p in item_list:
            add_info[p.split(':')[0].strip()] = p.split(':')[1].strip()
        # return add_info
        if search_term in add_info:
            return add_info[search_term]
        else:
            return 'NA'

    def close(self, reason):
        csv_file = max(glob.iglob('*.csv'), key=os.path.getctime)

        wb = Workbook()
        ws = wb.active

        with open(csv_file, 'r', encoding='utf-8') as f:
            for row in csv.reader(f):
                ws.append(row)

        wb.save(csv_file.replace('.csv', '') + '.xlsx')

    # @classmethod
    # def from_crawler(cls, crawler, *args, **kwargs):
    #     spider = super(AutopapaSpider, cls).from_crawler(crawler, *args, **kwargs)
    #     crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
    #     return spider

    # def spider_closed(self, spider):
    #     merge_all_to_a_book(glob.glob("output/output.csv"), "output/output.xlsx")
