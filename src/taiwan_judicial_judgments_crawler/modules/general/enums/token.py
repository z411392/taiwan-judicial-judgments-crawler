from typing import NewType


class Token:
    Court = NewType("Court", str)
    CaseType = NewType("CaseType", str)
    DateStr = NewType("DateStr", str)
    CaseNumber = NewType("CaseNumber", str)
