from dataclasses import dataclass, field

@dataclass
class Document:
    """Araştırma sistemine eklenen akademik veya tarihî belge."""

    title: str
    original_text: str
    author: str = "Bilinmiyor"
    language: str = "Belirtilmedi"
    period: str = "Belirtilmedi"
    source_type: str = "Belirtilmedi"
    translation: str = ""
    notes: list[str] = field(default_factory=list)
    analyses: list[str] = field(default_factory=list)
    def add_note(self, note: str) -> None:
        self.notes.append(note)

    def add_analysis(self, analysis: str) -> None:
        self.analyses.append(analysis)

    def report(self) -> str:
        return (
            f"\n--- BELGE KAYDI ---\n"
            f"Başlık: {self.title}\n"
            f"Yazar: {self.author}\n"
            f"Dil: {self.language}\n"
            f"Dönem: {self.period}\n"
            f"Kaynak türü: {self.source_type}\n"
            f"Orijinal metin: {self.original_text}\n"
            f"Çeviri: {self.translation or 'Henüz çevrilmedi'}\n"
            f"Not sayısı: {len(self.notes)}\n"
            f"Analiz sayısı: {len(self.analyses)}"
        )
