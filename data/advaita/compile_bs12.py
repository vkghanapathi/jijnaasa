#!/usr/bin/env python3
"""
Compile vyākhyā texts into bs12-as.md.
Inserts 5 commentaries (VN, RP, BM, PP, NY) after each bhāṣya section.
"""

import re

# Section extraction from vyākhyā files
# Each file has ## headers marking adhyāsa, sūtra 1, sūtra 2

VYAKHYA_ORDER = [
    ("vn", "वैयासिकन्यायमाला", "Bhāratītīrtha"),
    ("rp", "भाष्यरत्नप्रभा", "Govindānanda"),
    ("bm", "भामती", "Vācaspati Miśra"),
    ("pp", "पञ्चपादिका", "Padmapāda"),
    ("ny", "न्यायनिर्णय", "Ānandagiri"),
]

# VN section headers differ from others
VN_SECTIONS = {
    "adhyasa": "## प्रस्तावना",
    "sutra1": "## अधिकरणम् १",
    "sutra2": "## अधिकरणम् २",
}

OTHER_SECTIONS = {
    "adhyasa": "## अध्यासभाष्यव्याख्या",
    "sutra1": "## सूत्रम् १",
    "sutra2": "## सूत्रम् २",
}


def extract_sections(filepath, code):
    """Extract adhyāsa, sūtra 1, sūtra 2 sections from a vyākhyā file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if code == "vn":
        headers = VN_SECTIONS
    else:
        headers = OTHER_SECTIONS

    sections = {}
    for key, header in headers.items():
        # Find the header and extract text until the next ## header or end
        pattern = re.escape(header) + r'[^\n]*\n(.*?)(?=\n## |\Z)'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            sections[key] = match.group(1).strip()
        else:
            sections[key] = ""

    return sections


def build_vyakhya_block(section_key):
    """Build the combined vyākhyā block for a given section."""
    blocks = []
    for code, skt_name, eng_name in VYAKHYA_ORDER:
        filepath = f"vyakhya-{code}.md"
        sections = extract_sections(filepath, code)
        text = sections.get(section_key, "")
        if text:
            blocks.append(f"### {skt_name} ({eng_name})\n\n{text}")
    return "\n\n".join(blocks)


def main():
    # Read existing bhāṣya
    with open("bs12-as.md", 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Build the new file
    out = []

    # Lines 1-2: Headers
    out.append(lines[0].rstrip())  # प्रथमोऽध्यायः
    out.append(lines[1].rstrip())  # प्रथमः पादः

    # Lines 3-6: Adhyāsa Bhāṣya
    out.append("")
    out.append("## अध्यासभाष्यम्")
    out.append("")
    for i in range(2, 6):  # lines 3-6 (0-indexed: 2-5)
        out.append(lines[i].rstrip())

    # Adhyāsa vyākhyās
    out.append("")
    out.append("---")
    out.append("")
    out.append("## अध्यासभाष्यव्याख्याः")
    out.append("")
    out.append(build_vyakhya_block("adhyasa"))

    # Lines 7-13: Sūtra 1 (0-indexed: 6-12)
    out.append("")
    out.append("---")
    out.append("")
    for i in range(6, 13):
        out.append(lines[i].rstrip())

    # Sūtra 1 vyākhyās
    out.append("")
    out.append("---")
    out.append("")
    out.append("## सूत्रम् १ — व्याख्याः")
    out.append("")
    out.append(build_vyakhya_block("sutra1"))

    # Lines 14-18: Sūtra 2 (0-indexed: 13-17)
    out.append("")
    out.append("---")
    out.append("")
    for i in range(13, len(lines)):
        out.append(lines[i].rstrip())

    # Sūtra 2 vyākhyās
    out.append("")
    out.append("---")
    out.append("")
    out.append("## सूत्रम् २ — व्याख्याः")
    out.append("")
    out.append(build_vyakhya_block("sutra2"))

    # Write output
    with open("bs12-as.md", 'w', encoding='utf-8') as f:
        f.write("\n".join(out) + "\n")

    print("Done! bs12-as.md updated with all 5 vyākhyās.")


if __name__ == '__main__':
    main()
