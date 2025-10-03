from typing import Dict


class CaseTypeNormalizer:
    def __call__(self, case_type: str):
        s = case_type.strip()
        aliases: Dict[str, str] = {
            "民": "民事",
            "刑事": "刑事",
            "行政": "行政",
            "憲法": "憲法",
            "懲戒": "懲戒",
        }
        alias = aliases.get(s, s)
        case_type_selectors = {
            "民事": "民事",
            "刑事": "刑事",
            "行政": "行政",
            "憲法": "憲法",
            "懲戒": "懲戒",
        }
        case_type = case_type_selectors.get(alias, "民事")
        return case_type
