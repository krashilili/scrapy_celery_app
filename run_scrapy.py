from scrapy import cmdline
# cmdline.execute("scrapy crawl vendor_spider".split())
# cmdline.execute("scrapy crawl id_date_spider".split())
# cmdline.execute("scrapy crawl custom_spider -s LOG_FILE=custom_crawler.log".split())
cmdline.execute("scrapy crawl participant_spider -s LOG_FILE=participant_spider.log".split())