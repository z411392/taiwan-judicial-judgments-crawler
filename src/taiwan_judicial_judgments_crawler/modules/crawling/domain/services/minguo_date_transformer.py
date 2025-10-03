class MinguoDateTransformer:
    def __call__(self, date: str) -> str:
        year, month, day = map(int, date.split("-"))
        return year - 1911, month, day
