# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AutopapaItem(scrapy.Item):
    # define the fields for your item here like:
    production_year = scrapy.Field()
    nav_list = scrapy.Field()
    unique_name = scrapy.Field()
    nav_make = scrapy.Field()
    nav_series = scrapy.Field()
    nav_modal = scrapy.Field()
    gear_box = scrapy.Field()
    steering_wheel = scrapy.Field()
    seller = scrapy.Field()
    car_description = scrapy.Field()
    seller_comment = scrapy.Field()
    body_type = scrapy.Field()
    seller_phone = scrapy.Field()
    condition = scrapy.Field()
    engine_type = scrapy.Field()
    power = scrapy.Field()
    engine_volume = scrapy.Field()
    mileage = scrapy.Field()
    drive_wheels = scrapy.Field()
    doors = scrapy.Field()
    number_of_seats = scrapy.Field()
    color = scrapy.Field()
    model = scrapy.Field()
    price = scrapy.Field()
    # price_currency = scrapy.Field()
    customs = scrapy.Field()
    name = scrapy.Field()
    location = scrapy.Field()
    images = scrapy.Field()
    image_urls = scrapy.Field()

