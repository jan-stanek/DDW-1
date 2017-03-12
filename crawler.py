import scrapy

class Spider(scrapy.Spider):
    custom_settings = {
        'DOWNLOAD_DELAY': 1.5,
        'USER_AGENT': 'DDW',
        'ROBOTSTXT_OBEY': True,
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    name = 'www.krizovatka.skaut.cz'
    start_urls = ['https://krizovatka.skaut.cz/skautske-zakladny']

    def parse(self, response):
        realty_collection = response.css('.cwbase')
        if realty_collection:
            gps = realty_collection.css('.RealtyCollection .details').xpath('.//div[contains(strong,"GPS souřadnice:")]/text()').extract_first().split(' ')
            gps_lat = float(gps[0][:-1])
            gps_lon = float(gps[1][:-1])
            for realty in realty_collection.css('.OccupationAll .details'):
                description = realty.xpath('.//div[@class="spacer" or @class="detail"]')[0].xpath('.//text()').extract()
                description = ' '.join(description)
                yield {
                    'name': realty.css('h3 span ::text').extract_first(),
                    'gps_lat': gps_lat,
                    'gps_lon': gps_lon,
                    'type': realty.xpath('.//div[contains(strong,"Typ užívání:")]/text()').extract_first(),
                    'description': description
                }

        for next_realty in response.css('.category .button ::attr(href)').extract():
            yield scrapy.Request(response.urljoin(next_realty), callback=self.parse)

        for next_page in response.css('.pagination a ::attr(href)').extract():
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

