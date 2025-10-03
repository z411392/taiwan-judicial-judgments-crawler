class CourtNameNormalizer:
    def __call__(self, court: str):
        s = court.strip()
        s = s.replace("台", "臺")
        if "法院" not in s:
            s = f"{s}地方法院"
        if (
            not s.startswith("臺灣")
            and not s.startswith("福建")
            and not s.startswith("最高")
            and not s.startswith("智慧財產")
        ):
            s = f"臺灣{s}"
        return s
