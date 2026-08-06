from dataclasses import dataclass, field


@dataclass
class ResearchRequest:
    """Kullanıcının oluşturduğu akademik araştırma isteği."""

    topic: str
    level: str
    source_types: list[str] = field(default_factory=list)
    include_visuals: bool = False
    include_historical_texts: bool = False
    notes: str = ""

    def report(self) -> str:
        sources = ", ".join(self.source_types) or "Kaynak türü seçilmedi"

        return (
            "\n--- ARAŞTIRMA İSTEĞİ ---\n"
            f"Konu: {self.topic}\n"
            f"Seviye: {self.level}\n"
            f"Kaynaklar: {sources}\n"
            f"Görseller: {'Evet' if self.include_visuals else 'Hayır'}\n"
            f"Tarihî metinler: "
            f"{'Evet' if self.include_historical_texts else 'Hayır'}\n"
            f"Ek not: {self.notes or 'Yok'}"
        )
