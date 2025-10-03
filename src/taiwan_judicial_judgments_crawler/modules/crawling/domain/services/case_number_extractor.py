from re import search, sub


class CaseNumberExtractor:
    def __call__(self, title: str):
        """從標題中提取檔案名稱格式的案件編號，如 '附民字-1769'"""

        # 尋找字別和號數（不包含年度）
        # 格式: "臺灣高雄地方法院 113 年度 附民 字第 1769 號刑事裁定"
        pattern = r"(\d+)\s*年度\s*([^字]*字)第?\s*(\d+)\s*號"
        match = search(pattern, title)
        if match:
            _year, case_type, number = match.groups()
            return sub(r"\s+", "", f"{case_type}-{number}")
