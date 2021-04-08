from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leroy_merlin import settings
from leroy_merlin.spiders.leroymerlinru import LeroymerlinruSpider

if __name__ == '__main__':

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroymerlinruSpider, search='ершик%20для%20унитаза')

    process.start()