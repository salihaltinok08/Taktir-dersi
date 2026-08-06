from document import Document


def main():
    document = Document(
        title="Örnek Tarihî Belge",
        original_text="Bu alan belgenin özgün metnini içerir.",
        author="Bilinmeyen yazar",
        language="Osmanlı Türkçesi",
        period="19. yüzyıl",
        source_type="El yazması",
    )

    document.translation = (
        "Bu alan, tarihî belgenin günümüz Türkçesine çevrilmiş hâlidir."
    )

    document.add_note(
        "Belgenin yazarı kesin olarak tespit edilememiştir."
    )

    document.add_analysis(
        "Metin, dönemin inanç ve gündelik yaşam anlayışını yansıtıyor olabilir."
    )

    print(document.report())


if __name__ == "__main__":
    main()
