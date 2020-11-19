import scrapy
import pandas as pd
import json
from ..items import UkbookingsItem

class BookingsSpiderSpider(scrapy.Spider):
    name = 'bookings'
    offset = 0

    allowed_domains = ['booking.com']
    start_urls = ['https://www.booking.com/searchresults.html?aid=355028&sb=1&sb_lp=1&src=index&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Findex.html%3Faid%3D355028%3Bsb_price_type%3Dtotal%26%3B&ss=uk&is_ski_area=0&checkin_year=&checkin_month=&checkout_year=&checkout_month=&group_adults=2&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1&dest_id=&dest_type=&search_pageview_id=b7ca33f14d8000bd&search_selected=false']



    def parse(self, response):
        items = UkbookingsItem()
        hotel_name = response.css('div.sr_item:nth-of-type(n+2) span.sr-hotel__name').css('::text').extract()
        hotel_rating = response.css('div.sr_item:nth-of-type(n+2) div.bui-review-score__badge').css('::text').extract()
        hotel_review = response.css('div.bui-review-score__text').css('::text').extract()
        hotel_imagelink = response.css('div.sr_item:nth-of-type(n+2) img.hotel_image::attr(src)').extract()

        items['hotel_name'] = hotel_name
        items['hotel_rating'] = hotel_rating
        items['hotel_review'] = hotel_review
        items['hotel_imagelink'] = hotel_imagelink

        yield items

        next_page = 'https://www.booking.com/searchresults.html?aid=355028&tmpl=searchresults&class_interval=1&dest_id=222&dest_type=country&dtdisc=0&from_sf=1&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=1&postcard=0&room1=A%2CA&sb_price_type=total&search_pageview_id=b7ca33f14d8000bd&shw_aparth=1&slp_r_match=0&src=index&src_elem=sb&srpvid=4c4172f667ad0023&ss=uk&ss_all=0&ssb=empty&sshis=0&top_ufis=1&rows=25&offset='+ str(BookingsSpiderSpider.offset)

        if BookingsSpiderSpider.offset <= 1000:
            BookingsSpiderSpider.offset += 25
            yield response.follow(next_page, callback = self.parse)


            with open("items.json") as file:
                data = json.load(file)

            fname = "UKbookings.csv"
            df = pd.json_normalize(data)
            df.to_csv(fname,"a",index=False)
            print (df)