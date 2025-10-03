from taiwan_judicial_judgments_crawler.modules.crawling.domain.ports.driven.judgement_repository import (
    JudgementRepository,
)
from os import makedirs
from os.path import exists
from aiofiles import open as aio_open
from pathlib import Path


class JudgementFileSystemAdapter(JudgementRepository):
    async def save(
        self,
        path: str,
        text: str,
    ):
        dir = Path(path).parent
        if not exists(dir):
            makedirs(dir)
        async with aio_open(path, "w", encoding="utf-8") as handle:
            await handle.write(text)
