from research import ResearchRequest
from sources import search_crossref
from storage import load_sources, save_sources

def ask_yes_no(question: str) -> bool:
    answer = input(f"{question} (e/h): ").strip().lower()
    return answer == "e"


def main():
    print("=" * 45)
    print("TAKDİR DERSİ - AKADEMİK ARAŞTIRMA")
    print("=" * 45)

    topic = input("Araştırmak istediğiniz konu: ").strip()
    level = input(
        "Araştırma seviyesi "
        "(ortaokul/lise/lisans/yüksek lisans/doktora): "
    ).strip()

    source_input = input(
        "Kaynak türlerini virgülle ayırarak yazın "
        "(makale, kitap, tez, arşiv, müze): "
    ).strip()

    source_types = [
        item.strip()
        for item in source_input.split(",")
        if item.strip()
    ]

    include_visuals = ask_yes_no(
        "Görseller dahil edilsin mi?"
    )

    include_historical_texts = ask_yes_no(
        "Tarihî metinler dahil edilsin mi?"
    )

    notes = input(
        "Ek araştırma notunuz varsa yazın: "
    ).strip()

    request = ResearchRequest(
        topic=topic,
        level=level,
        source_types=source_types,
        include_visuals=include_visuals,
        include_historical_texts=include_historical_texts,
        notes=notes,
    )

    print(request.report())

    print("\nAkademik kaynaklar aranıyor...")

    try:
        sources = search_crossref(
            topic=request.topic,
            limit=5,
        )
    except (ValueError, RuntimeError) as error:
        print(f"\nKaynak araması başarısız oldu: {error}")
        return
    save_sources(sources)

    if not sources:
        print("\nBu konu için kaynak bulunamadı.")
        return

    print(
        f"\n--- BULUNAN AKADEMİK KAYNAKLAR "
        f"({len(sources)}) ---"
    )

    for number, source in enumerate(
        sources,
        start=1,
    ):
        print(f"\nKAYNAK {number}")
        print("-" * 40)
        print(source.report())

    saved_sources = load_sources()

    print(
        f"\n{len(saved_sources)} kaynak cihaz hafızasına kaydedildi."
    )


if __name__ == "__main__":
    main()

