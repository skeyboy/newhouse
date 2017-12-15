from scrapy import cmdline

cmdline.execute("scrapy crawl NewHouse -o items.json".split())