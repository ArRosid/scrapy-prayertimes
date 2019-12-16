# -*- coding: utf-8 -*-
import scrapy


class PrayerTimeLastMonthSpider(scrapy.Spider):
    page = 1
    name = 'prayer_time_last_month'
    allowed_domains = ['www.jadwalsholat.org']
    start_urls = [f'https://www.jadwalsholat.org/adzan/monthly.php?id={page}/']

    def parse(self, response):
        result = {}
        
        city = response.xpath("//h1[@class='h1_edit']/text()").get().split()[3].strip(",")
        month_year = response.xpath("//h2[@class='h2_edit']/text()").get()
        
        result["city"] = city
        result["data"] = []

        rows = response.xpath("//tr[@class='table_light' or @class='table_dark' or @class='table_highlight']")

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

        self.page = self.page + 1

        if self.page <= 307:
            yield scrapy.Request(url=f'https://www.jadwalsholat.org/adzan/monthly.php?id={self.page}/',
                                callback=self.parse)


        
