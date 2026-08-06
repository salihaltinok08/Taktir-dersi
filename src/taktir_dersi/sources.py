from dataclasses import dataclass
from typing import Any

import requests


CROSSREF_API_URL = "https://api.crossref.org/works"


@dataclass
class AcademicSource:
    title: str
    authors: list[str]
    year: int | None
    source_name: str
    doi: str | None
    url: str | None
    source_type: str

    def report(self) -> str:
        author_text = ", ".join(self.authors) or "Yazar bilinmiyor"
        year_text = str(self.year) if self.year else "Yıl bilinmiyor"

        return (
            f"Başlık: {self.title}\n"
            f"Yazar: {author_text}\n"
            f"Yıl: {year_text}\n"
            f"Yayın: {self.source_name or 'Bilinmiyor'}\n"
            f"Tür: {self.source_type or 'Bilinmiyor'}\n"
            f"DOI: {self.doi or 'Yok'}\n"
            f"Bağlantı: {self.url or 'Yok'}"
        )


def _first_text(value: Any, default: str = "") -> str:
    if isinstance(value, list) and value:
        return str(value[0])

    if isinstance(value, str):
        return value

    return default


def _extract_year(item: dict[str, Any]) -> int | None:
    date_fields = (
        "published-print",
        "published-online",
        "published",
        "issued",
    )

    for field_name in date_fields:
        date_parts = item.get(field_name, {}).get("date-parts", [])

        if date_parts and date_parts[0]:
            year = date_parts[0][0]

            if isinstance(year, int):
                return year

    return None


def _extract_authors(item: dict[str, Any]) -> list[str]:
    authors = []

    for author in item.get("author", []):
        given = str(author.get("given", "")).strip()
        family = str(author.get("family", "")).strip()
        full_name = f"{given} {family}".strip()

        if full_name:
            authors.append(full_name)

    return authors


def search_crossref(
    topic: str,
    limit: int = 5,
) -> list[AcademicSource]:
    if not topic.strip():
        raise ValueError("Araştırma konusu boş bırakılamaz.")

    params = {
        "query": topic,
        "rows": limit,
        "select": (
            "title,author,published-print,published-online,"
            "published,issued,container-title,DOI,URL,type"
        ),
    }

    headers = {
        "User-Agent": (
            "TaktirDersi/0.1 "
            "(academic research application)"
        )
    }

    try:
        response = requests.get(
            CROSSREF_API_URL,
            params=params,
            headers=headers,
            timeout=20,
        )
        response.raise_for_status()
    except requests.RequestException as error:
        raise RuntimeError(
            "Crossref bağlantısı sırasında hata oluştu."
        ) from error

    items = response.json().get("message", {}).get("items", [])
    results = []

    for item in items:
        results.append(
            AcademicSource(
                title=_first_text(
                    item.get("title"),
                    "Başlık bilinmiyor",
                ),
                authors=_extract_authors(item),
                year=_extract_year(item),
                source_name=_first_text(
                    item.get("container-title"),
                ),
                doi=item.get("DOI"),
                url=item.get("URL"),
                source_type=str(item.get("type", "")),
            )
        )

    return results
