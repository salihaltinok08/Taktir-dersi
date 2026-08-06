import json
from dataclasses import asdict
from pathlib import Path

from sources import AcademicSource


DATA_DIRECTORY = Path("data")
SOURCES_FILE = DATA_DIRECTORY / "sources.json"


def save_sources(sources: list[AcademicSource]) -> None:
    """Akademik kaynakları JSON dosyasına kaydeder."""

    DATA_DIRECTORY.mkdir(exist_ok=True)

    source_data = [
        asdict(source)
        for source in sources
    ]

    with SOURCES_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            source_data,
            file,
            ensure_ascii=False,
            indent=2,
        )


def load_sources() -> list[AcademicSource]:
    """Daha önce kaydedilen akademik kaynakları yükler."""

    if not SOURCES_FILE.exists():
        return []

    with SOURCES_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        source_data = json.load(file)

    return [
        AcademicSource(**item)
        for item in source_data
    ]
