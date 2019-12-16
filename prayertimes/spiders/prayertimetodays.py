# -*- coding: utf-8 -*-
import scrapy


class PrayertimetodaysSpider(scrapy.Spider):
    page = 1
    name = 'prayertimetodays'
    allowed_domains = ['www.jadwalsholat.org']
    start_urls = [f'https://www.jadwalsholat.org/adzan/monthly.php?id={page}']
    
    def parse(self, response):
        city = response.xpath('//h1[@class="h1_edit"]/text()').get().split()[3].strip(",")
        month_years = response.xpath('//h2[@class="h2_edit"]/text()').get()
        day = response.xpath('//tr[@class="table_highlight"]/td[1]/b/text()').get()
        imsyak = response.xpath('//tr[@class="table_highlight"]/td[2]/text()').get()
        shubuh = response.xpath('//tr[@class="table_highlight"]/td[3]/text()').get()
        terbit = response.xpath('//tr[@class="table_highlight"]/td[4]/text()').get()
        dhuha = response.xpath('//tr[@class="table_highlight"]/td[5]/text()').get()
        dzuhur = response.xpath('//tr[@class="table_highlight"]/td[6]/text()').get()
        ashr = response.xpath('//tr[@class="table_highlight"]/td[7]/text()').get()
        maghrib = response.xpath('//tr[@class="table_highlight"]/td[8]/text()').get()
        isya = response.xpath('//tr[@class="table_highlight"]/td[9]/text()').get()

        yield {
            "city": city,
            "date": f"{day}, {month_years}",
            "imsyak": imsyak,
            "shubuh": shubuh,
            "terbit": terbit,
            "dhuha": dhuha,
            "dzuhur": dzuhur,
            "ashr": ashr,
            "maghrib": maghrib,
            "isya": isya
        }

        self.page = self.page + 1

        if self.page <= 307:
            yield scrapy.Request(url=f'https://www.jadwalsholat.org/adzan/monthly.php?id={self.page}',
                                callback=self.parse)


