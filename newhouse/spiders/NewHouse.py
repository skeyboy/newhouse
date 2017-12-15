# -*- coding: utf-8 -*-
import scrapy
from newhouse.items import AreaModelItem, RailModelItem, StationModelItem, HouseModelItem
import sqlite3

host = "http://newhouse.zz.fang.com"
start = "http://newhouse.zz.fang.com/house/s/"

class NewhouseSpider(scrapy.Spider):
    name = "NewHouse"
    # allowed_domains = ["http://newhouse.zz.fang.com/"]
    start_urls = [start]
    db = sqlite3.connect('./newhouse.db')

    def parse(self, response):

        sql = """CREATE TABLE if NOT EXISTS house(ID INTEGER PRIMARY KEY   AUTOINCREMENT ,kind VARCHAR , address VARCHAR , em VARCHAR , href VARCHAR UNIQUE  , img VARCHAR , name VARCHAR    , price VARCHAR , state VARCHAR , tel VARCHAR , value_num VARCHAR )"""
        self.db.execute(sql)
        self.db.commit()



        pages = response.xpath('//div[@class="page"]//li[@class="fr"]/a[@class="next"]')
        last = response.xpath('//div[@class="page"]//li[@class="fr"]/a[@class="last"]')
        if len(pages) or len(last):
            current_page = \
                response.xpath('//div[@class="page"]//li[@class="fr"]/a[@class="active"]/text()').extract()[
                    0]
            if current_page.isdigit() == False:
                return

            for page in pages:
                href = page.xpath("@href").extract()[0]
                if current_page.isdigit():
                    #             http://newhouse.zz.fang.com/house/s/jinshui1/b93/?ctm=1.zz.xf_search.page.5
                    real_href = host + href + "?ctm=1.zz.xf_search.page." + str(int(current_page) + 1)
                    print(real_href)
                    yield scrapy.Request(url=real_href, callback=self.parse_hous_list)

    def parse_hous_list(self, response):

        # id = "newhouse_loupai_list"
        houses = response.xpath('//div[@id="newhouse_loupai_list"]/ul/li')

        # print(houses)
        house_items = []
        for house in houses:
            house_model = HouseModelItem()
            name = house.xpath('div/div[@class="nlc_details"]/div/div[@class="nlcd_name"]/a/text()').extract()[0]
            name = name.strip().strip("\t").strip(",")

            house_model['name'] = name
            imgs = house.xpath('div/div[@class="nlc_img"]/a/img/@src').extract()
            if len(imgs) == 2:
                house_model['img'] = imgs[1]
            else:
                house_model['img'] = imgs[0]

            hrefs = house.xpath('div/div[@class="nlc_img"]/a/@href').extract()
            if len(hrefs) == 2:

                house_model['href'] = hrefs[1]
            else:
                house_model['href'] = hrefs[0]

            try:
                house_model['price'] = house.xpath('div/div[@class="nlc_details"]/div[@class="nhouse_price"]/span/text()').extract()[0]
            except:
                print("暂无价格")
                house_model['price'] = "暂无价格"

            house_model['image_urls'] = house_model['img']

            em = house.xpath('div/div[@class="nlc_details"]/div[@class="nhouse_price"]/em/text()').extract()
            if len(em) > 0:
                house_model['em'] = em[0]
            else:
                house_model['em'] = '价格待定'
            state = house.xpath('div/div[@class="nlc_details"]//span[@class="forSale"]/text()').extract()
            if len(state) == 0:
                state = house.xpath('div/div[@class="nlc_details"]//span[@class="inSale"]/text()').extract()
            # if state is not None:
            if state:

                house_model['state'] = state[0]
            else:
                house_model['state'] = "暂无状态"
            try:
                house_model['kind'] = house.xpath('div/div[@class="nlc_details"]//div[@class="fangyuan pr"]/a').xpath("string(.)").extract()[0]
            except:
                print("没有类型")
                house_model['kind'] = "没有类型"

            house_model['address'] = \
                house.xpath('div/div[@class="nlc_details"]//div[@class="address"]/a/@title').extract()[0]
            try:
                house_model['value_num'] = \
                    house.xpath('div/div[@class="nlc_details"]//span[@class="value_num"]/text()').extract()[0]
            except:
                print("暂无评论")
                house_model['value_num'] = "暂无评论"


            try:
                house_model['tel'] = house.xpath(
                    'div/div[@class="nlc_details"]/div[@class="relative_message clearfix"]/div[@class="tel"]/p').xpath("string(.)").extract()[0]
            except:
                print("没有电话号码")
                house_model['tel'] = "没有电话号码"


            commite = []
            house_items.append((house_model['address'], house_model['em'], house_model['href'], house_model['img'],
                                house_model['name'], house_model['price'], house_model['state'], house_model['tel'],
                                house_model['value_num']))
            yield house_model

        try:
            self.db.executemany(
                'INSERT INTO house(address, em,href,img, name, price, state, tel, value_num) VALUES (?,?,?,?,?,?,?,?,?)',
                house_items)

            self.db.commit()


        except Exception as e:
            self.db.rollback()
            # print(house_model)
            print(house_model['name']+response.url)

            print(e)

        try:
            pages = response.xpath('//div[@class="page"]//li[@class="fr"]/a[@class="next"]')
            last = response.xpath('//div[@class="page"]//li[@class="fr"]/a[@class="last"]')
            next = response.xpath('//div[@class="page"]//li[@class="fr"]/a[@class="next"]')

            print("页面：",pages)

            # 先检查是否有next，否则检查其他策略
            if False:
                next_href = next.xpath("@href").extract()[-1]
                real_href = host + next_href + "?ctm=1.zz.xf_search.page"

                yield scrapy.Request(url=real_href, callback=self.parse_hous_list)
            else:
                if pages is None:
                    print("错误啊")

                if len(pages) and len(last):
                    # print(pages)

                    current_page = \
                        response.xpath('//div[@class="page"]//li[@class="fr"]/a[@class="active"]/text()').extract()[
                            0]
                    if current_page.isdigit() == False:
                        return

                    page = pages[-1]

                    # for page in pages:
                    href = page.xpath("@href").extract()[0]
                    # if current_page.isdigit():
                    #             http://newhouse.zz.fang.com/house/s/jinshui1/b93/?ctm=1.zz.xf_search.page.5
                    real_href = host + href + "?ctm=1.zz.xf_search.page"
                    print("原始网站:"+response.url)
                    print(real_href)
                    yield scrapy.Request(url=real_href, callback=self.parse_hous_list)
                else:
                    if len(pages) and len(last)==0:
                        pages

                    print("结束没有数据了")
                    return
        except  :
            print("意外结束")
