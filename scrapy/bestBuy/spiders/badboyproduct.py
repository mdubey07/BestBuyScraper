# -*- coding: utf-8 -*-
import scrapy
import json


class BadboyproductSpider(scrapy.Spider):
    name = 'badboyproduct'
    allowed_domains = ['badboymowers.com']

    # start_urls = ['http://badboymowers.com/']

    def start_requests(self):
        p_urls = self.get_urls()

        for p in p_urls:
            yield scrapy.Request(url=p.p_url, callback=self.parse, meta={'category': p.p_cat})

    def parse(self, response):
        product_container = response.css('div#main-content')
        product_description_head1 = product_container.css('div.align-items-center div.px-lg-5 h2.my-lg-4::text').get()
        product_description = product_container.css('div.align-items-center div.px-lg-5 p.lead::text').get()
        product_description = product_description.encode('ascii', 'xmlcharrefreplace').decode('utf8')
        description = '<strong>' + product_description_head1 + '</strong>' + "\n" + str(product_description) + "\n"

        feature_container = product_container.css('div#features')
        modal_name = feature_container.css('div.orange-bg h5 span.heading::text').get()
        tab_heading = []
        tab_content = []
        for f_tab in feature_container.css('div.orange-bg ul#myTab li'):
            tabhead = f_tab.css('a span::text').get()
            tabhead = '<strong>' + tabhead + '</strong>' + "\n"
            tab_heading.append(tabhead)

        for f_tab_content in feature_container.css('div.orange-bg div.tab-content div.tab-pane'):
            # tabcontent = f_tab_content.css('p::text').get()
            tabcontent = f_tab_content.css('p::text').getall()
            # converting the special chars to html entities
            encodedlist = []
            for x in tabcontent:
                tt = x.encode('ascii', 'xmlcharrefreplace').decode('utf8')
                encodedlist.append(tt)
            # adding newline in both side of tab contents
            encodedlist = "\n\n".join(encodedlist)
            tab_content.append(encodedlist)
        final_features = ''
        for i in range(len(tab_heading)):
            final_features = final_features + tab_heading[i] + tab_content[i] + "\n\n"
        photos = ''
        photo_container = product_container.css('div#photos')
        for photo in photo_container.css('div.no-gutters div.recent-news-block'):
            photo_url = 'https://www.badboymowers.com' + photo.css('a > img.img-fluid::attr(src)').get()
            photos = photos + photo_url + ','
        photos = photos[:-1]

        spec_container = product_container.css('div#specs')
        spec_tables = ''
        format_cols_data = []
        for spec_table in spec_container.css('div.mower-spec-table-container table.mower-spec-table'):
            spec_tables_heading = '\'' + spec_table.css('thead tr h6::text').get() + '\''
            cols = []
            temp = ''
            m = 1
            for sdata in spec_table.css('tbody tr'):
                for tds in sdata.css('td'):
                    if m % 2 == 0:
                        # tdata = sdata.css('td span.text-orange::text').get()
                        tdata = tds.css(' ::text').extract()
                        tdata = ''.join(tdata)
                        temp = temp + '\'' + tdata.encode('ascii', 'xmlcharrefreplace').decode('utf8') + '\':'
                        temp = temp[:-1]
                        cols.append(temp)
                        temp = ''
                    else:
                        # tdata = sdata.css('td::text').get()
                        tdata = tds.css('::text').get()
                        temp = temp + '\'' + tdata.encode('ascii', 'xmlcharrefreplace').decode('utf8') + '\':'
                    m = m + 1
            cols_string = ','.join(cols)
            spec_table_row = spec_tables_heading + ':{' + cols_string + '}'
            format_cols_data.append(spec_table_row)
        spec_tables = ','.join(format_cols_data)
        spec_tables = '{' + spec_tables + '}'

        yield {
            'Model': modal_name,
            'Brand': "Bad Boy Mowers",
            'category': response.meta.get('category'),
            'Category image': "",
            'Subcategory': "",
            'Subcategory image': "",
            'Series': "",
            'Series image': "",
            'Product images': photos,
            'Description': description,
            'Specs': spec_tables,
            'Features': final_features,
            'url': '',
        }

    def get_urls(self):
        p_urls = []
        with open('badboyurls.json', encoding="utf8") as jsonFile:
            json_data = json.load(jsonFile)
            for data in json_data:
                cat_name = data['category']
                product_url = data['url']
                p_urls.append(Product(cat_name, product_url))
        return p_urls


class Product:
    def __init__(self, category, url):
        self.p_cat = category
        self.p_url = url
