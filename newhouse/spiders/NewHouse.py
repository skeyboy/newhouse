# -*- coding: utf-8 -*-
import scrapy
# from newhouse.model import AreaModelItem
from newhouse.items import AreaModelItem, RailModelItem, StationModelItem, HouseModelItem

host = "http://newhouse.zz.fang.com"


class NewhouseSpider(scrapy.Spider):
    name = "NewHouse"
    # allowed_domains = ["http://newhouse.zz.fang.com/"]
    start_urls = ['http://newhouse.zz.fang.com/house/s/']

    def parse(self, response):
        rails = self.parse_rail(response)

        areas = self.parse_area(response.xpath('//dd[@class="lp_area"]//a'))

        for area in areas:
            yield scrapy.Request(url=area['href'], callback=self.parse_hous_list)

        for rail in rails:
            yield scrapy.Request(url=rail['href'], callback=self.parse_rail_subs)


    def parse_hous_list(self, response):

        # 是否有下一页
        pages = response.xpath('//div[@class="page"]//li[@class="fr"]/a[@class="next"]')

        if len(pages):
            # print(pages)

            current_page = response.xpath('//div[@class="page"]//li[@class="fr"]/a[@class="active"]/text()').extract()[
                0]
            for page in pages:
                href = page.xpath("@href").extract()[0]
                if current_page.isdigit():
                    #             http://newhouse.zz.fang.com/house/s/jinshui1/b93/?ctm=1.zz.xf_search.page.5
                    real_href = host + href + "?ctm=1.zz.xf_search.page." + str(int(current_page)+1)
                    print(real_href)
                    yield scrapy.Request(url=real_href, callback=self.parse_hous_list)

        # id = "newhouse_loupai_list"
        houses = response.xpath('//div[@id="newhouse_loupai_list"]/ul/li')

        # print(houses)
        for house in houses:
            house_model = HouseModelItem()
            house_model['name'] = house.xpath('//div[@class="nlcd_name"]/a/text()').extract()[0]
            house_model['img'] = house.xpath('//div[@class="nlc_img"]/a/img/@src').extract()[1]
            house_model['price'] = house.xpath('//div[@class="nhouse_price"]/span/text()').extract()[0]
            em = house.xpath('//div[@class="nhouse_price"]/em/text()').extract()
            if len(em) > 0:
                house_model['em'] = em[0]
            state = house.xpath('//div[@class="nlc_details"]//span[@class="forSale"]/text()').extract()
            if len(state) == 0:
                state = house.xpath('//div[@class="nlc_details"]//span[@class="inSale"]/text()').extract()
            # if state is not None:

            house_model['state'] = state[0]
            # house_model['kind'] = house.xpath('//div[@class="nlc_details"]//div[@class="fangyuan pr"]/a/text()').extract()[0]

            house_model['address'] = \
                house.xpath('//div[@class="nlc_details"]//div[@class="address"]/a/@title').extract()[0]
            house_model['value_num'] = \
                house.xpath('//div[@class="nlc_details"]//span[@class="value_num"]/text()').extract()[0]
            house_model['tel'] = house.xpath(
                '//div[@class="nlc_details"]/div[@class="relative_message clearfix"]/div[@class="tel"]/p/text()').extract()[
                0]

            print(house_model)


    def parse_rail_subs(self, response):
        # //*[@id="sjina_D03_06"]/div/ol/li/a[1]
        rail_subs = response.xpath('//dd[@ctm-data="lpsearch_rail"]//ol//a')
        for station in rail_subs:
            index = 5
            stationMode = StationModelItem()
            # http://newhouse.zz.fang.com/house/s/b439-b51330-b7rail/?ctm=1.zz.xf_search.lpsearch_rail.6
            stationMode['href'] = host + station.xpath('@href').extract()[
                0] + "?ctm=1.zz.xf_search.lpsearch_rail." + str(index)
            stationMode['station'] = station.xpath('text()').extract()[0]
            stationMode['index'] = index
            index = index + 1
            # print(stationMode)
            yield scrapy.Request(url=stationMode['href'], callback=self.parse_hous_list)



    def parse_area(self, area):
        # print(area)
        areas = []
        index = 1
        for area_item in area:
            # print(area_item.xpath("@href").extract()[0])
            # print(area_item.xpath("text()").extract()[0])

            # http://newhouse.zz.fang.com/house/s/jinshui1/?ctm=1.zz.xf_search.lpsearch_area.2
            area_model = AreaModelItem()
            area_model['index'] = index
            area_model['area'] = area_item.xpath("text()").extract()[0]
            area_model['href'] = host + area_item.xpath("@href").extract()[
                0] + "?ctm=1.zz.xf_search.lpsearch_area." + str(index)
            index = index + 1
            areas.append(area_model)
            # print(area_model)
        return areas


    def parse_rail(self, response):
        rails = []
        rail = response.xpath('//dd[@ctm-data="lpsearch_rail"]//a')
        # print("地铁")
        rail_index = 1

        for rail_item in rail:
            rail_model = RailModelItem()
            rail_model['index'] = rail_index
            rail_model['rail'] = rail_item.xpath('text()').extract()[0]

            # http://newhouse.zz.fang.com/house/s/b439-b7rail/?ctm=1.zz.xf_search.lpsearch_rail.2
            rail_model['href'] = host + rail_item.xpath('@href').extract()[
                0] + '?ctm=1.zz.xf_search.lpsearch_rail.' + str(rail_index)
            if rail_index >= 2:
                rails.append(rail_model)
                # yield scrapy.Request(url=rail_model['href'], callback=self.parse_rail_subs)

            rail_index = 1 + rail_index

        # print(rails)
        return rails
