# -*- coding: utf-8 -*-
import scrapy


class DistanceDirectionToMakkahSpider(scrapy.Spider):
    page = 1
    name = 'distance_direction_to_makkah'
    allowed_domains = ['www.jadwalsholat.org']
    start_urls = [f'https://www.jadwalsholat.org/adzan/monthly.php?id={page}/']

    def parse(self, response):
        city_name = response.xpath('//h1[@class="h1_edit"]/text()').get().split()[3].strip(",")
        distance = response.xpath("(//tr[@class='table_block_content'])[3]/td[@colspan='5']/text()").get().split()[0]
        direction = response.xpath("(//tr[@class='table_block_content'])[2]/td[@colspan='5']/text()").get().split()[0]

        yield {
            "city": city_name,
            "distance": distance,
            "direction": direction
        }

        self.page = self.page + 1

        if self.page <= 307:
            yield scrapy.Request(url=f'https://www.jadwalsholat.org/adzan/monthly.php?id={self.page}/',
                            callback=self.parse)