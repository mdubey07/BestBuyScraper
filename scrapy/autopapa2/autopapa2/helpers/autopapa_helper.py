import wget
import os


class AutopapaHelper:
    helper_response = None

    def get_production_year(self):
        production_year = self.helper_response.xpath(
            '//*[@class="InfoObject"]//div[@class="nameInfoObject"]//text()').extract()
        if production_year:
            production_year = production_year[1]
            return production_year
        else:
            return None

    def get_body_type(self):
        body_type = self.helper_response.xpath(
            '//*[@class="InfoObject"]//div[@class="nameInfoObject"]//text()').extract()
        if body_type:
            body_type = body_type[3]
            return body_type
        else:
            return None

    def get_condition(self):
        condition = self.helper_response.xpath(
            '//*[@class="InfoObject"]//div[@class="nameInfoObject"]//text()').extract()
        if condition:
            condition = condition[5]
            return condition
        else:
            return None

    def get_engine_type(self):
        engine_type = self.helper_response.xpath(
            '//*[@class="InfoObject"]//div[@class="nameInfoObject"]//text()').extract()
        if engine_type:
            engine_type = engine_type[7]
            return engine_type
        else:
            return None

    def get_engine_volume(self):
        engine_volume = self.helper_response.xpath(
            '//*[@class="InfoObject"]//div[@class="nameInfoObject"]//text()').extract()
        if engine_volume:
            engine_volume = engine_volume[11]
            return engine_volume
        else:
            return None

    def get_power(self):
        power = self.helper_response.xpath(
            '//*[@class="InfoObject"]//div[@class="nameInfoObject"]//text()').extract()
        if power:
            power = power[9]
            return power
        else:
            return None

    def get_mileage(self):
        mileage = self.helper_response.xpath(
            '//*[@class="InfoObject InfoObjectRight"]//div[@class="nameInfoObject"]//text()').extract()
        if mileage:
            mileage = mileage[1]
            return mileage
        else:
            return None

    def get_drive_wheels(self):
        drive_wheels = self.helper_response.xpath(
            '//*[@class="InfoObject InfoObjectRight"]//div[@class="nameInfoObject"]//text()').extract()
        if drive_wheels:
            drive_wheels = drive_wheels[3]
            return drive_wheels
        else:
            return None

    def get_doors(self):
        doors = self.helper_response.xpath(
            '//*[@class="InfoObject InfoObjectRight"]//div[@class="nameInfoObject"]//text()').extract()
        if doors:
            doors = doors[5]
            return doors
        else:
            return None

    def get_number_of_seats(self):
        number_of_seats = self.helper_response.xpath(
            '//*[@class="InfoObject InfoObjectRight"]//div[@class="nameInfoObject"]//text()').extract()
        if number_of_seats:
            number_of_seats = number_of_seats[7]
            return number_of_seats
        else:
            return None

    def get_color(self):
        color = self.helper_response.xpath(
            '//*[@class="InfoObject InfoObjectRight"]//div[@class="nameInfoObject"]//text()').extract()
        if color:
            color = color[9]
            return color
        else:
            return None

    def get_model(self):
        model = self.helper_response.xpath(
            '//*[@class="InfoObject InfoObjectRight"]//div[@class="nameInfoObject"]//text()').extract()
        if model and len(model) == 13:

            model = model[-1]
            return model
        else:
            return None

    # def get_price(self):
    #     price = self.helper_response.xpath(
    #         '//*[@class="priceObject"]/text()').extract_first()
    #     return price

    def get_price(self):
        price = self.helper_response.css('span.priceObject::text').extract_first()
        if price:
            price = price.replace(' ', '')
        return price.strip()

    # def get_price_currency(self):
    #     price_currency = self.helper_response.css('span.priceObject::text').get()
    #     if price_currency:
    #         price_currency = price_currency[:1]
    #     return price_currency.strip()

    def get_name(self):
        name = self.helper_response.xpath(
            '//*[@class="titleObject"]/text()').extract_first()
        return name.strip()

    def get_location(self):
        location = self.helper_response.xpath(
            '//*[@class="contactObjectNew"]/div/text()').extract_first()
        return location.strip()

    def get_customs(self):
        customs = self.helper_response.xpath(
            '//*[@class="contactObjectNew"]//nobr/text()').extract_first()
        return customs.strip()

    def get_seller(self):
        seller = self.helper_response.xpath(
            '//*[@class="contactObjectNew"]/div/text()').extract()
        if seller:
            seller = seller[2].strip()
            seller = seller.split(',')[0]
            return seller
        else:
            return seller

    def get_seller_phone(self):
        seller_phone = self.helper_response.xpath(
            '//*[@class="contactObjectNew"]/div/a/text()').extract_first()
        return seller_phone.strip()

    def get_car_description(self):
        car_description = self.helper_response.xpath(
            '//*[@class="comment-all"]/text()').extract_first()
        if car_description:
            return car_description.strip()
        else:
            return None

    def get_seller_comment(self):
        seller_comment = self.helper_response.xpath(
            '//*[@class="comment-seller"]/text()').extract()
        if seller_comment:
            return seller_comment[-1].strip()
        else:
            return None

    def get_unique_name(self):
        unique_name = self.helper_response.css('ul#nav3 li:last-child::text').extract()
        if unique_name:
            unique_name = self.rm_whilespace(unique_name)
            return unique_name
        else:
            return None

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

    def get_nav_list(self):
        nav_list2 = self.helper_response.css('ul#nav3 li')
        # temp_list = str(len(nav_list2)) + '-'
        temp_list = []
        for nav_li in nav_list2:
            li_text = nav_li.css('a::text').get()
            if li_text:
                temp_list.append(li_text.strip())
        if temp_list:
            temp_list.pop(0)
            # temp_list = '|'.join(temp_list)
            return temp_list
        else:
            return None

    # def get_nav_make(self):
    #     nav_make = self.helper_response.css('ul#nav3 li:nth-of-type(2) a::text').extract_first()
    #     if nav_make:
    #         nav_make = nav_make.strip()
    #         return nav_make
    #     else:
    #         return None
    #
    # def get_nav_series(self):
    #     nav_series = self.helper_response.css('ul#nav3 li:nth-of-type(3) a::text').extract_first()
    #     if nav_series:
    #         nav_series = nav_series.strip()
    #         return nav_series
    #     else:
    #         return None
    #
    # def get_nav_model(self):
    #     nav_model = self.helper_response.css('ul#nav3 li:nth-of-type(4) a::text').extract_first()
    #     if nav_model:
    #         nav_model = nav_model.strip()
    #         return nav_model
    #     else:
    #         return None

    def get_images(self):
        images = self.helper_response.xpath(
            '//*[@class="boxImgGallery image"]/a/@href').extract()
        original_images = []
        for image in images:
            if '?' in image:
                image = f'https://autopapa.ge{image}'
                # image_path = self.dowload_image(image)
                original_images.append(image)

        return original_images

    # def get_images(self):
    #     images = self.helper_response.xpath(
    #         '//*[@class="boxImgGallery image"]/a/@href').extract()
    #     original_images = []
    #     for image in images:
    #         if '?' in image:
    #             image = f'https://autopapa.ge{image}'
    #             image_path = self.dowload_image(image)
    #             original_images.append(image_path)
    #
    #     return original_images
    #
    # def dowload_image(self, image_url):
    #     image_name = image_url.split('?')[-1]
    #     image_path = f'output/images/{image_name}.jpg'
    #     wget.download(image_url, image_path)
    #     return image_path
