from injector import Injector
from httpx import AsyncClient as HttpConnectionPool
from time import tzset
from taiwan_judicial_judgments_crawler.utils.logging.setup_logging import setup_logging


async def startup():
    tzset()
    setup_logging()
    from taiwan_judicial_judgments_crawler.modules.crawling import crawling_module
    from taiwan_judicial_judgments_crawler.modules.general import general_module

    injector = Injector([crawling_module, general_module])
    injector.binder.bind(HttpConnectionPool, HttpConnectionPool())
    return injector
