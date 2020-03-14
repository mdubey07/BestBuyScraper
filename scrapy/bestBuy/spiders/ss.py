# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime, timedelta
import os
import csv
import glob
from openpyxl import Workbook


class SsSpider(scrapy.Spider):
    name = 'ss'
    allowed_domains = ['ss.ge']
    start_urls = ['https://ss.ge/ka/udzravi-qoneba/l?PriceType=false&CurrencyId=1']
    order_by = '&Sort.SortExpression=%22OrderDate%22%20DESC'
    by_prop_id = '&Context.Request.Query%5BQuery%5D='
    prop_query = '&Query='
    currentDate = str(datetime.now().date())
    currentDate = datetime.strptime(currentDate.strip(), "%Y-%m-%d")
    # date_start = "18.02.2020"
    # end_date = "05.02.2020"
    property_ids = []

    def start_requests(self):
        if len(self.property_ids) > 0:
            for pid in self.property_ids:
                url = self.start_urls[0] + self.prop_query + pid.strip() + self.by_prop_id + pid.strip()
                yield scrapy.Request(url=url, callback=self.parse)
        else:
            yield scrapy.Request(url=self.start_urls[0], callback=self.parse)

    def parse(self, response):
        for single_property in response.css('div.latest_article_each'):
            l_link = single_property.css('.DesktopArticleLayout .latest_desc > div > a::attr(href)').get()
            ab_link = response.urljoin(l_link)
            l_price = single_property.css('.DesktopArticleLayout .latest_price::text').extract_first()
            if l_price:
                l_price = l_price.strip()
            else:
                l_price = 'NA'
            l_symbol = single_property.css('.DesktopArticleLayout .latest_price .PriceCurreny::text').extract_first()
            if l_symbol:
                l_symbol = l_symbol.strip()
            else:
                l_symbol = 'NA'
            if ab_link:
                yield scrapy.Request(ab_link, callback=self.parse_page, meta={'l_price': l_price, 'l_symbol': l_symbol})

        next_p = response.xpath('//*[@class="next"]//@href').extract_first()
        if next_p:
            next_p = response.urljoin(next_p)
            yield scrapy.Request(next_p, callback=self.parse)

    @staticmethod
    def rm_whilespace(query_term):
        if query_term:
            None_ = [nn_.replace('\n', '') for nn_ in query_term]
            None_ = [nn_.strip() for nn_ in None_]
            None_ = filter(None, None_)
            None_ = ' '.join(None_)
            ret_value = None_
            return ret_value
        # query_term = query_term.encode('ascii', 'xmlcharrefreplace').decode('utf8')
        return query_term

    def parse_page(self, response):
        url = response.url
        title = response.xpath('//*[@class="article_in_title"]//text()').extract()
        title = self.rm_whilespace(title)

        article_item_id = response.xpath('//*[@class="article_item_id"]//text()').extract()
        article_item_id = self.rm_whilespace(article_item_id)

        article_views = response.xpath('//*[@class="article_views"]//text()').extract()
        article_views = self.rm_whilespace(article_views)

        add_date_block = response.xpath('//*[@class="add_date_block"]//text()').extract()
        add_date_block = self.rm_whilespace(add_date_block)
        # add_date_block = ''.join(add_date_block)
        propertyDate = self.ss_date(add_date_block)

        Total_Area = response.xpath(
            '//*[@class="ParamsBotBlk"][contains(text(),"საერთო ფართი")]//preceding-sibling::div[@class="ParamsHdBlk"]//text()').extract()
        Total_Area = self.rm_whilespace(Total_Area)

        Rooms = response.xpath(
            '//*[@class="ParamsBotBlk"][contains(text(),"ოთახები")]//preceding-sibling::div[@class="ParamsHdBlk"]//text()').extract()
        Rooms = self.rm_whilespace(Rooms)

        Bedrooms = response.xpath(
            '//*[@class="ParamsBotBlk"][contains(text(),"საძინებლები")]//preceding-sibling::div[@class="ParamsHdBlk"]//text()').extract()
        Bedrooms = self.rm_whilespace(Bedrooms)

        Floor = response.xpath(
            '//*[@class="ParamsBotBlk"][contains(text(),"სართული")]//preceding-sibling::div[@class="ParamsHdBlk"]//text()').extract()
        Floor = self.rm_whilespace(Floor)

        Project = response.xpath(
            '//*[@class="TitleEachparbt"][contains(text(), "პროექტი")]//following-sibling::*[@class="PRojeachBlack"]//text()').extract()
        Project = self.rm_whilespace(Project)

        State = response.xpath(
            '//*[@class="TitleEachparbt"][contains(text(), "მდგომარეობა")]//following-sibling::*[@class="PRojeachBlack"]//text()').extract()
        State = self.rm_whilespace(State)

        Status = response.xpath(
            '//*[@class="TitleEachparbt"][contains(text(), "სტატუსი")]//following-sibling::*[@class="PRojeachBlack"]//text()').extract()
        Status = self.rm_whilespace(Status)

        Addi_info_avi = response.xpath('//*[@class="AditionalInfoBlocksBody"]')
        Addi_info_avi = Addi_info_avi.xpath('.//*[@class="CheckedParam"]//following-sibling::text()').extract()
        Addi_info_avi = '|'.join(Addi_info_avi)

        Addi_info_un_avi = response.xpath('//*[@class="AditionalInfoBlocksBody"]')
        Addi_info_un_avi = Addi_info_un_avi.xpath('.//*[@class="UnCheckedParam"]//following-sibling::text()').extract()
        # Addi_info_un_avi = [item.replace(",", "|") for item in Addi_info_un_avi]
        Addi_info_un_avi = '|'.join(Addi_info_un_avi)

        desc = response.xpath('//*[@class="details_text"]//text()').extract()
        desc = self.rm_whilespace(desc)

        price = response.css('.desktopPriceBlockDet div.article_right_price::text').extract()
        price = self.rm_whilespace(price)

        author = response.xpath('//*[@class="author_type"]/text()').extract()
        author = self.rm_whilespace(author)

        tel = response.xpath('//*[@class="EAchPHonenumber BeforeClickedHidden"]//@href').extract_first()
        number = ''
        if tel:
            number = tel.replace('tel:', '')

        img = response.xpath('//*[@class="item"]//img//@src').extract()
        img = [nn_.replace('\n', '') for nn_ in img]
        img = [nn_.strip() for nn_ in img]
        img = filter(None, img)
        img = ', '.join(img)
        img = img

        ptype = response.css('.detailed_page_navlist li:nth-of-type(2) a::text').extract_first()
        if ptype:
            ptype = ptype.strip()

        pstatus = response.css('.detailed_page_navlist li:nth-of-type(3) a::text').extract_first()
        if pstatus:
            pstatus = pstatus.strip()

        city = response.css('.detailed_page_navlist li:nth-of-type(4) a::text').extract_first()
        other_locations = response.xpath('//*[@class="StreeTaddressList"]//a//text()').extract_first()
        if city:
            city = city.strip()
        if other_locations:
            other_locations = other_locations.strip()

        region = response.css('.detailed_page_navlist li:nth-of-type(5) a::text').extract_first()
        if region:
            region = region.strip()

        # if (propertyDate >= self.ss_date(self.date_start)) and (propertyDate <= self.ss_date(self.end_date)):
        if propertyDate == self.currentDate or len(self.property_ids) > 0:
            yield {
                'img': img,
                'title': title,
                'article_item_id': article_item_id,
                'pstatus': pstatus,
                'Total_Area': Total_Area,
                'Rooms': Rooms,
                'Bedrooms': Bedrooms,
                'Floor': Floor,
                'Project': Project,
                'State': State,
                'Status': Status,
                'Addi_info_avi': Addi_info_avi,
                'Addi_info_un_avi': Addi_info_un_avi,
                'desc': desc,
                'price': price,
                'Latest Price': response.meta.get('l_price'),
                'price Currency': response.meta.get('l_symbol'),
                'author': author,
                'number': number,
                'ptype': ptype,
                'city': city,
                'region': region,
                'street': other_locations,
                'Property_date': propertyDate,
                'url': url,
            }

    @staticmethod
    def ss_date(sdate):
        sep = '/'
        output = str(sdate)
        output = output.split(sep, 1)[0]
        output.strip()
        date_object = datetime.strptime(output.strip(), "%d.%m.%Y")
        return date_object

    def close(self, reason):
        csv_file = max(glob.iglob('*.csv'), key=os.path.getctime)

        wb = Workbook()
        ws = wb.active

        with open(csv_file, 'r', encoding='utf-8') as f:
            for row in csv.reader(f):
                ws.append(row)

        wb.save(csv_file.replace('.csv', '') + '.xlsx')
