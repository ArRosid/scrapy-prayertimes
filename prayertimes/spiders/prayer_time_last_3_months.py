# -*- coding: utf-8 -*-
import scrapy


class PrayerTimeLast3MonthsSpider(scrapy.Spider):
    city_page = 1
    month_page = 1
    name = 'prayer_time_last_3_months'
    allowed_domains = ['www.jadwalsholat.org']
    start_urls = [f'https://www.jadwalsholat.org/adzan/monthly.php?id={city_page}/']

    def parse(self, response):

        result = {}

        city_name = response.xpath("//h1[@class='h1_edit']/text()").get().split()[3].strip(",")
        month_year = response.xpath("//h2[@class='h2_edit']/text()").get()

        result["city_name"] = city_name
        result["data"] = []

        rows = response.xpath('//tr[@class="table_light" or @class="table_dark" or @class="table_highlight"]')

        for row in rows:
            date = row.xpath(".//td[1]/b/text()").get()
            imsyak = row.xpath(".//td[2]/text()").get()
            shubuh = row.xpath(".//td[3]/text()").get()
            terbit = row.xpath(".//td[4]/text()").get()
            dhuha = row.xpath(".//td[5]/text()").get()
            dzuhur = row.xpath(".//td[6]/text()").get()
            ashr = row.xpath(".//td[7]/text()").get()
            maghrib = row.xpath(".//td[8]/text()").get()
            isya = row.xpath(".//td[9]/text()").get()

            result["data"].append({
                "date": f"{date}, {month_year}",
                "imsyak": imsyak,
                "shubuh": shubuh,
                "terbit": terbit,
                "dhuha": dhuha,
                "dzuhur": dzuhur,
                "ashr": ashr,
                "maghrib": maghrib,
                "isya": isya
            })

        yield result

        next_page = response.xpath("//a[@title='sebelum']/@href").get() # Get next page
        if self.month_page < 3:
            if next_page:
                yield response.follow(url=next_page, callback=self.parse)
            self.month_page = self.month_page + 1


        else: #if already scrape for 3 last month
            self.city_page = self.city_page + 1 # move to next city
            if self.city_page <= 307:
                self.month_page = 1 # selet next month page count to 1 if move to next city
                yield scrapy.Request(url=f'https://www.jadwalsholat.org/adzan/monthly.php?id={self.city_page}/',
                                    callback=self.parse)

