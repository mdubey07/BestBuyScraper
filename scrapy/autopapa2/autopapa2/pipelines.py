import csv


# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class AutopapaPipeline(object):

    def process_item(self, item, spider):
        return item

    # def __init__(self):
    #     # file_path = 'output/output.csv'
    #     file_path = 'G:/Projects/MyPython/BestBuyScraper/scrapy/autopapa2/autopapa2/output/output.csv'
    #     csvfile = open(file_path, 'w')
    #     fieldnames = ['name',
    #                   'location',
    #                   'price',
    #                   'production_year',
    #                   'seller',
    #                   'body_type',
    #                   'seller_phone',
    #                   'condition',
    #                   'engine_type',
    #                   'power',
    #                   'engine_volume',
    #                   'mileage',
    #                   'drive_wheels',
    #                   'doors',
    #                   'number_of_seats',
    #                   'color',
    #                   'customs',
    #                   'model',
    #                   'car_description',
    #                   'seller_comment',
    #                   'images']
    #     self.writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
    #     self.writer.writeheader()
    #
    # def process_item(self, item, spider):
    #     self.writer.writerow(item)
    #     return item
