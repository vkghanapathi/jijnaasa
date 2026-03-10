#!/usr/bin/env python3
"""
Fetch vyākhyā texts for BS 1.1.1-1.1.2 from Advaita Sharada.
Extracts: भाष्यरत्नप्रभा, भामती, पञ्चपादिका, वैयासिकन्यायमाला, न्यायनिर्णय
"""

import re
import sys
import time
import urllib.request
from html.parser import HTMLParser

BASE_URL = "https://advaitasharada.sringeri.net"

VYAKHYAS = {
    "RP": "भाष्यरत्नप्रभा (Govindānanda)",
    "BM": "भामती (Vācaspati Miśra)",
    "PP": "पञ्चपादिका (Padmapāda)",
    "VN": "वैयासिकन्यायमाला (Bhāratītīrtha)",
    "NY": "न्यायनिर्णय (Ānandagiri)",
}


class HTMLTextExtractor(HTMLParser):
    """Extract text from HTML, preserving paragraph structure."""
    def __init__(self):
        super().__init__()
        self.result = []
        self.current_class = None
        self.in_tag = False
        self.skip = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'p':
            cls = attrs_dict.get('class', '')
            self.current_class = cls
            self.in_tag = True
            if cls == 'prateeka':
                self.result.append('\n**')
            elif cls == 'Avataranika':
                self.result.append('\n')
            elif cls == 'Vyakhya':
                self.result.append('')
        elif tag == 'div':
            cls = attrs_dict.get('class', '')
            if 'VyakhyaDescriptor' in cls:
                self.result.append('\n---\n')
        elif tag == 'br':
            self.result.append('\n')

    def handle_endtag(self, tag):
        if tag == 'p' and self.in_tag:
            if self.current_class == 'prateeka':
                self.result.append('**\n')
            else:
                self.result.append('\n')
            self.in_tag = False
            self.current_class = None

    def handle_data(self, data):
        text = data.strip()
        if text:
            self.result.append(text)

    def handle_entityref(self, name):
        if name == 'nbsp':
            self.result.append(' ')

    def get_text(self):
        return ''.join(self.result).strip()


def fetch_url(url):
    """Fetch URL content."""
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (scholarly research)'
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode('utf-8')


def get_section_ids(vyakhya_code):
    """Get section IDs for a vyakhya from the main page."""
    url = f"{BASE_URL}/display/bhashyaVyakhya/BS/devanagari?vyakhya={vyakhya_code}"
    html = fetch_url(url)
    # Extract vyakhyaPara data attribute
    match = re.search(r'data-vyakhya="' + vyakhya_code + r'">(.*?)</div>', html, re.DOTALL)
    if match:
        all_ids = match.group(1).strip().split(';')
        # Filter for BS 1.1.1 and 1.1.2 only
        # I01-I04 = Adhyāsa Bhāṣya intro
        # V01_* = Sūtra 1
        # V02_* = Sūtra 2
        filtered = []
        for sid in all_ids:
            sid = sid.strip()
            if not sid:
                continue
            if re.match(r'BS_C01_S01_I\d+$', sid):
                filtered.append(sid)
            elif re.match(r'BS_C01_S01_V01_', sid):
                filtered.append(sid)
            elif re.match(r'BS_C01_S01_V02_', sid):
                filtered.append(sid)
        return filtered
    return []


def fetch_vyakhya_section(vyakhya_code, section_id):
    """Fetch vyakhya text for a single section."""
    url = f"{BASE_URL}/display/getVyakhya/{vyakhya_code}/{section_id}"
    html = fetch_url(url)
    extractor = HTMLTextExtractor()
    extractor.feed(html)
    return extractor.get_text()


def main():
    for code, name in VYAKHYAS.items():
        print(f"\n{'='*60}")
        print(f"Fetching {name} ({code})...")
        print(f"{'='*60}")

        section_ids = get_section_ids(code)
        print(f"  Found {len(section_ids)} sections for BS 1.1.1-1.1.2")

        if not section_ids:
            print(f"  WARNING: No sections found for {code}")
            continue

        output_file = f"vyakhya-{code.lower()}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# {name}\n")
            f.write(f"## ब्रह्मसूत्रभाष्यव्याख्या — सूत्र १.१.१–१.१.२\n\n")
            f.write(f"Source: [Advaita Sharada]({BASE_URL}/display/bhashyaVyakhya/BS/devanagari?vyakhya={code})\n\n")

            current_section_type = None
            for i, sid in enumerate(section_ids):
                # Add section headers
                if re.match(r'BS_C01_S01_I', sid) and current_section_type != 'intro':
                    f.write(f"\n## अध्यासभाष्यव्याख्या\n\n")
                    current_section_type = 'intro'
                elif re.match(r'BS_C01_S01_V01_', sid) and current_section_type != 'v01':
                    f.write(f"\n## सूत्रम् १ — अथातो ब्रह्मजिज्ञासा\n\n")
                    current_section_type = 'v01'
                elif re.match(r'BS_C01_S01_V02_', sid) and current_section_type != 'v02':
                    f.write(f"\n## सूत्रम् २ — जन्माद्यस्य यतः\n\n")
                    current_section_type = 'v02'

                print(f"  [{i+1}/{len(section_ids)}] Fetching {sid}...")
                try:
                    text = fetch_vyakhya_section(code, sid)
                    if text:
                        f.write(text)
                        f.write('\n\n')
                except Exception as e:
                    print(f"    ERROR: {e}")
                    f.write(f"\n[Error fetching {sid}: {e}]\n\n")

                # Be polite to the server
                time.sleep(0.3)

        print(f"  Saved to {output_file}")

    print("\nDone!")


if __name__ == '__main__':
    main()
