from os import getenv
from pathlib import Path
from taiwan_judicial_judgments_crawler.modules.general.enums.token import Token
from injector import inject


class OutputPathCalculator:
    _root: Path
    _case_type: Token.CaseType
    _court: Token.Court
    _date_str: Token.DateStr

    @inject
    def __init__(
        self,
        case_type: Token.CaseType,
        court: Token.Court,
        date_str: Token.DateStr,
    ):
        self._root = Path(getenv("ROOT_PATH"))
        self._case_type = case_type
        self._court = court
        self._date_str = date_str

    def __call__(self, file_name: str):
        dir = (
            self._root / "data" / self._case_type / self._court / self._date_str
        ).resolve()
        return f"{dir}/{file_name}"
