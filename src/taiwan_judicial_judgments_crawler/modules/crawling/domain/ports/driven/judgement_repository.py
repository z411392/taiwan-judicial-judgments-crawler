from abc import ABC, abstractmethod
from typing import Awaitable


class JudgementRepository(ABC):
    @abstractmethod
    def save(path: str, text: str) -> Awaitable[None]:
        raise NotImplementedError()
