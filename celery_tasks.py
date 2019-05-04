from celery.app.base import Celery
# from celery.contrib import rdb
from billiard.context import Process
from scrapy.utils.project import get_project_settings
from celery.utils.log import get_task_logger
from scrapy.crawler import CrawlerProcess
# import user spiders
#from Crawlers.spiders import


# Create celery app
celery_app = Celery('tasks',
                    broker='redis://localhost:6379/0',
                    backend='redis://localhost:6379/0')
celery_app.config_from_object('celeryconfig')


class UrlCrawlerScript(Process):
        def __init__(self, spider):
            Process.__init__(self)
            settings = get_project_settings()
            self.crawler = CrawlerProcess(settings)
            # self.crawler.configure()
            # self.crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
            self.spider = spider

        def run(self):
            self.crawler.crawl(self.spider)
            self.crawler.start()
            # reactor.run()


def run_spider():
    # user spider
    # spider = CustomSpider()
    crawler = UrlCrawlerScript(spider)
    crawler.start()
    crawler.join()
    return "Done"


@celery_app.task
def crawl(**kwargs):
    print("Args: ")
    print(kwargs)
    return run_spider(**kwargs)


# test function
@celery_app.task
def add(a,b):
    x= a+b
    return x