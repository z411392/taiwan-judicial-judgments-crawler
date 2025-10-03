from bs4 import BeautifulSoup
from re import sub


class TextParser:
    def _clean_text(self, text: str):
        return sub(r"\s", "", text.replace("\u3000", "").replace("\xa0", " "))

    def _parse_table(self, soup: BeautifulSoup):
        for th, td in zip(soup.select(".col-th"), soup.select(".col-td")):
            th_text = self._clean_text(th.get_text(strip=True))
            td_text = self._clean_text(td.get_text(strip=True))
            yield th_text + td_text

    def _parse_paragraphs(self, soup: BeautifulSoup):
        div = soup.select("[id*=paragraph]")
        for tag in div:
            text = tag.get_text(strip=True)
            cleaned = self._clean_text(text)
            yield cleaned

    def __call__(self, raw: str):
        soup = BeautifulSoup(raw, "html.parser").select_one("#jud")
        soup.attrs = {}
        table = "\n".join(self._parse_table(soup))
        paragraphs = "\n".join(self._parse_paragraphs(soup))
        return table + paragraphs
