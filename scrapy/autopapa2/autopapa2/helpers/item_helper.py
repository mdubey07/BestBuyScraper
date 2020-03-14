from ..items import AutopapaItem


class ItemHelper:

    def make_item(self,
                  production_year=None,
                  nav_list=None,
                  unique_name=None,
                  nav_make=None,
                  nav_series=None,
                  nav_modal=None,
                  gear_box=None,
                  steering_wheel=None,
                  condition=None,
                  engine_type=None,
                  power=None,
                  engine_volume=None,
                  mileage=None,
                  drive_wheels=None,
                  doors=None,
                  number_of_seats=None,
                  color=None,
                  model=None,
                  price=None,
                  # price_currency=None,
                  name=None,
                  seller=None,
                  customs=None,
                  seller_phone=None,
                  car_description=None,
                  seller_comment=None,
                  location=None,
                  body_type=None,
                  # images=None,
                  image_urls=None
                  ):
        item = AutopapaItem()
        item['production_year'] = production_year
        item['nav_list'] = nav_list
        item['unique_name'] = unique_name
        item['nav_make'] = nav_make
        item['nav_series'] = nav_series
        item['nav_modal'] = nav_modal
        item['gear_box'] = gear_box
        item['steering_wheel'] = steering_wheel
        item['condition'] = condition
        item['seller_comment'] = seller_comment
        item['car_description'] = car_description
        item['seller'] = seller
        item['seller_phone'] = seller_phone
        item['body_type'] = body_type
        item['engine_type'] = engine_type
        item['power'] = power
        item['mileage'] = mileage
        item['drive_wheels'] = drive_wheels
        item['doors'] = doors
        item['number_of_seats'] = number_of_seats
        item['color'] = color
        item['model'] = model
        item['engine_volume'] = engine_volume
        item['price'] = price
        # item['price_currency'] = price_currency
        item['name'] = name
        item['customs'] = customs
        item['location'] = location
        # item['images'] = images
        item['image_urls'] = image_urls

        return item
