"""
Jijñāsā Adhikaraṇa — A Critical Review
Brahma Sūtra 1.1.1: अथातो ब्रह्मजिज्ञासा

Thesis: National Sanskrit University, Tirupati
Researcher: N. Kuvalaya Datta
Supervisor: Prof. MLN Bhat
Consultant: Dr. Vamśīkṛṣṇa Ghanapāṭhī

A critical review of the Dvaita (Nyāya Sudhā) refutation of Advaita Siddhānta
in the Jijñāsā Adhikaraṇa, establishing the soundness of the Advaita method.

Source Texts:
  1. Nyāya Sudhā with prominent commentaries (Dvaita)
  2. Śārīraka Mīmāṃsā Bhāṣya with Ānandagiri Ṭīkā (Advaita)
  3. Dhvānta Nirāsa (Advaita)
  4. Other useful treatises

Output: ~300 pages in Classical Sanskrit
  - 6 batches: intro, 4 chapters, conclusion
"""

# Thesis structure
THESIS_STRUCTURE = {
    "batch_1": {
        "section": "Front Matter",
        "contents": ["Index", "Acknowledgments", "Tributes"],
    },
    "batch_2": {
        "section": "Introduction",
        "contents": [
            "Scope and methodology",
            "Source texts and editions used",
            "Historical context of the Dvaita-Advaita debate",
            "Structure of the Jijñāsā Adhikaraṇa",
        ],
    },
    "batch_3": {
        "section": "Chapter 1 — Pūrvapakṣa",
        "contents": [
            "The Dvaita position as presented in Nyāya Sudhā",
            "Madhvācārya's reading of अथातो ब्रह्मजिज्ञासा",
            "The Dvaita refutation of Advaita on this sūtra",
        ],
    },
    "batch_4": {
        "section": "Chapter 2 — Critical Analysis",
        "contents": [
            "Logical examination of the Dvaita refutation",
            "Identification of reasoning gaps and inconsistencies",
            "Assessment of the soundness of their arguments",
        ],
    },
    "batch_5": {
        "section": "Chapter 3 — Advaita Siddhānta",
        "contents": [
            "Śaṅkara Bhāṣya on the Jijñāsā Sūtra",
            "Ānandagiri Ṭīkā — elaboration and defence",
            "Dhvānta Nirāsa — counter-refutation of Dvaita objections",
        ],
    },
    "batch_6": {
        "section": "Chapter 4 — Synthesis",
        "contents": [
            "Establishing the Advaita method's logical superiority",
            "Comparative assessment of both interpretive frameworks",
            "The pristine sound vs. the noise",
        ],
    },
    "batch_7": {
        "section": "Conclusion & Back Matter",
        "contents": ["Summary of findings", "Bibliography", "Appendices"],
    },
}

SOURCE_TEXTS = {
    "dvaita": [
        "Nyāya Sudhā (न्यायसुधा) — Jayatīrtha's commentary on Madhva's Brahma Sūtra Bhāṣya",
    ],
    "advaita": [
        "Śārīraka Mīmāṃsā Bhāṣya (शारीरकमीमांसाभाष्यम्) — Śaṅkarācārya",
        "Ānandagiri Ṭīkā (आनन्दगिरि टीका) — gloss on Śaṅkara Bhāṣya",
        "Dhvānta Nirāsa (ध्वान्तनिरासः) — Advaita counter-refutation",
    ],
}


def main():
    print("=" * 60)
    print("  Jijñāsā Adhikaraṇa — A Critical Review")
    print("  Brahma Sūtra 1.1.1: अथातो ब्रह्मजिज्ञासा")
    print("=" * 60)
    print()
    print("  National Sanskrit University, Tirupati")
    print("  Researcher : N. Kuvalaya Datta")
    print("  Supervisor  : Prof. MLN Bhat")
    print("  Consultant  : Dr. Vamśīkṛṣṇa Ghanapāṭhī")
    print()

    print("Thesis Structure:")
    print("-" * 40)
    for batch_id, batch in THESIS_STRUCTURE.items():
        print(f"  {batch_id}: {batch['section']}")
        for item in batch["contents"]:
            print(f"    - {item}")
    print()

    print("Source Texts:")
    print("-" * 40)
    for tradition, texts in SOURCE_TEXTS.items():
        print(f"  [{tradition.upper()}]")
        for text in texts:
            print(f"    - {text}")


if __name__ == "__main__":
    main()
