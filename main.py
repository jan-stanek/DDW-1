from scrapy import cmdline
cmdline.execute("scrapy runspider crawler.py -o data.json".split())