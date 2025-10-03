from taiwan_judicial_judgments_crawler.modules.crawling.presentation.cli.handlers.handle_scan import (
    handle_scan,
)
from injector import Injector
from types import MethodType


def create_entrypoints(injector: Injector):
    return dict(
        scan=MethodType(handle_scan, injector),
    )
