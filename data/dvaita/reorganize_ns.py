#!/usr/bin/env python3
"""
Reorganize bs-ns12.md into thesis-ready format with:
- Topic-by-topic structure with N.1, N.2 numbering
- AV verse boxes (markdown tables)
- Empty Samīkṣā (review) boxes
- Two main sections: Jijñāsādhikaraṇa and Janmādhikaraṇa
"""

import re
import sys

INPUT  = '/Users/dharmaposhanam/Documents/GitHub/Jijnaasa/data/dvaita/bs-ns12.md'
OUTPUT = '/Users/dharmaposhanam/Documents/GitHub/Jijnaasa/data/dvaita/bs-ns12.md'

# ── regex patterns ──────────────────────────────────────────────────
PAGE_RE      = re.compile(r'^\*[०-९0-9,\s\.]+\*\s*$')
NS_MARKER_RE = re.compile(r'^न्यायसुधा\s*$')
AV_END_RE    = re.compile(r'>\s*$')
COLOPHON_RE  = re.compile(r'^॥\s.*॥\s*$')
SEPARATOR_RE = re.compile(r'^[_━═─]+\s*$')
SUTRA_RE     = re.compile(r'BBस्')
SENT_END_RE  = re.compile(r'[।॥]\s*$')
SHLOKA_NUM   = re.compile(r'^\s*\d+\s*॥')  # verse numbering like ७॥

# ── known heading line numbers (1-indexed) ──────────────────────────
# Curated from analysis. These are the definitive topic heading lines.
HEADING_LINES = {
    # ── जिज्ञासाधिकरणम् (BS 1.1.1) ──
    2,      # मङ्गलाचरणम्
    41,     # नम्यत्वप्रयोजकधर्मपरतया व्याख्यानम्
    81,     # लक्षणपरतया व्याख्यानम्
    96,     # निखिलेत्याद्युक्तलक्षणोपपन्नतया...
    107,    # बाधकनिरासपरतया व्याख्यानम्
    117,    # सकलशास्त्रार्थपरतया व्याख्यानम्
    131,    # गुरुत्वेन व्यासस्य प्रणामः
    166,    # व्याख्येयत्वसमर्थनम्
    200,    # आगमेन शास्त्रप्रामाण्यम्
    242,    # विद्याशास्त्रशब्दयोः समानार्थत्वम्
    251,    # प्रामाण्यमात्रे अनुमानम्
    262,    # हेतूनां साक्षात्साध्यनिर्देशः
    292,    # हेतूणामव्यभिचरितत्वम्
    304,    # साध्यान्तराध्याहारसमर्थनम्
    309,    # तथात्वे प्रामाण्यं त्रिविधम
    311,    # उपाद्युद्भावमसंगतम्
    337,    # कोऽयमाप्तः
    361,    # आप्तिस्वरूपनिरूपणम्
    377,    # आप्तेः लक्षणान्तरम्
    391,    # मध्ये किमाप्तवाक्यतासाधनम्
    416,    # भाष्यकृतः परम्पराश्रयणे निमित्तम्
    425,    # यच्छ्रुतिसंवादियच्चयुक्तिसंवादितत्प्रमाणम्
    475,    # ब्रह्मसूत्राणामेव त्रिविधं प्रामाण्यम्
    504,    # प्रामाण्योक्तिसमर्थनम्
    527,    # स्पष्टार्थः
    561,    # मङ्गलवादः
    608,    # अथशब्दो मङ्गलार्थः
    634,    # भामतीविवरणमतविमर्शः
    666,    # ओंकारः सूत्रावयवः
    690,    # प्रयोजनाद्यभिधानं सार्थकम्
    712,    # आदिमसूत्रस्य शास्त्रान्तर्भावः
    751,    # कः पुनरस्य सूत्रस्य प्रसङ्गः
    770,    # जिज्ञासायाः कर्तव्यत्वचिन्तनम्
    791,    # न अनात्मविषयेयं जिज्ञासा
    811,    # न स्वात्मपरात्मपरमात्मविषयेयं जिज्ञासा
    829,    # न चेश्वरविषया जिज्ञासा
    854,    # प्रयोजनाभावान्नजिज्ञासाकर्तव्या
    891,    # ईश्वर एव शास्त्रस्य विषयः
    904,    # गुणपूर्णतैव ओंकारस्यार्थः
    915,    # यौगिकशब्दानामवयवसंगतिग्रहणापेक्षा आवश्यकी
    924,    # ओंकारब्रह्मशब्दयोः न अभेदोऽर्थः
    934,    # गुणोततेतिरूपः साधुः
    949,    # नारायणपदस्यापि गुणपूर्णतैवार्थः
    977,    # ईश्वरः वेदेन प्रमितः
    1008,   # गायत्र्यर्थः नारायण एव
    1034,   # स सर्वा वाक्साक्षातोंकारव्याख्यानम्
    1055,   # मीमांसाद्वारा शास्त्रस्यापि ईश्वरविषयकत्वम्
    1083,   # निर्णयप्रयोजकत्वात्मीमांसायाः ईश्वरविषयत्वम्
    1100,   # कर्मणि षष्ठीपरिग्रहः षष्टिसमासविचारः
    1124,   # कर्मप्राधान्यार्थं जिज्ञास्य इति प्रयोगः
    1129,   # कर्तव्येतिपदाध्याहारविचारः
    1139,   # गतार्थताशङ्कातत्समाधानानुपपत्ति प्रदर्शनम्
    1154,   # जिज्ञासाया निष्प्रयोजनत्वनिरासः
    1231,   # ज्ञानमोक्षयोर्मध्ये प्रसादानपेक्षत्वशङ्का
    1258,   # मोक्षस्य हर्यधीनत्वम्
    1274,   # बन्धस्येश्वराधीनत्वोपपादनम्
    1297,   # ईश्वरप्रसादस्यापेक्षितत्वसमर्थनम्
    1318,   # विवरणमतानुवादः
    1339,   # विवरणमतनिरासः
    1427,   # टीकाकृत्स्वयं समाधत्ते
    1462,   # सिद्धान्तेबन्धनिवृत्तिसमर्थनम्
    1499,   # बन्धमिथ्यात्ववर्णनम्
    1516,   # बन्धमिथ्यात्वं प्रयोजनविषयोपपादकम्
    1586,   # बन्ध्मिथ्यात्वं विनापि मुक्तिर्घटते
    1618,   # विवरणोक्तबाधकपरिहारः
    1639,   # मुक्तिः बन्धमिथ्यात्वं नैवापेक्षत
    1731,   # मिथ्यात्वस्य प्रत्यक्षविरोधः
    1770,   # नेह नानास्तीति श्रुत्यर्थविचारः
    1899,   # असतः साधकत्वभङ्ग
    1966,   # असतः साधकत्वाभावे बाधकोद्धारः
    2010,   # सिद्धान्ते नेह नानेति श्रुत्यर्थसमर्थनम्
    2037,   # अविशेषस्य साधकत्वभङ्गः
    2126,   # प्रमाण्यादिसत्तानभ्युपगमे वादित्वानुपपत्तिः
    2153,   # जिज्ञासाधिकरणे प्रमाणादिसत्तानभ्युपगमे वादित्वानुपपत्तिः
    2326,   # व्यावहारिकसत्यस्य साधकत्वभङ्गः
    2388,   # सत्त्रैविध्ये अनिर्वचनीये च प्रमाणनिरासः
    2637,   # परमते सत्वनिरुक्तभङ्गः
    2682,   # पराभिमतबाध्यत्वखण्डनम्
    2726,   # बाध्यत्वनिर्वचनम्
    2785,   # अनिर्वचनीयलक्षणनिरासः
    2842,   # प्रभाकरेण परिणामपक्षानुवादः
    3171,   # प्रभाकराख्यातिनिरासः
    3534,   # रामानुजाख्यात्यनुवादः

    # ── जन्माधिकरणम् (BS 1.1.2) ──
    3570,   # अथ मायावाद्युक्तस्य निर्गुणत्वस्यापि सूत्रकारैरेव निराकृतता
    3578,   # जगज्जन्मादिकारणत्वस्य तटस्थत्वकल्पना
    3607,   # जगज्जन्मादिकारणत्वस्य तटस्थत्वकल्पना अयुक्ता
    3711,   # अथ तदुक्तस्य "गुणगुणिनोः अन्यत्वानन्यत्वाभ्यामनिरूपणम्"इत्यस्य दुष्टता
    3995,   # अन्यवादिभिरपि विशेषोऽङ्गीकार्यः
    4073,   # यथाऽहुः
}

# First line of Janmādhikaraṇa section
JANMA_START = 3570

# ── Additional headings detected by heuristic ──────────────────────
# Lines that look like headings but aren't in the manual set.
# We'll detect them and include them.
EXTRA_SKIP = set()  # Lines to force-skip as NOT headings (false positives)

def is_heading_heuristic(line_stripped, line_num, in_av):
    """Detect lines that look like topic headings via heuristic."""
    s = line_stripped
    if not s or in_av:
        return False
    if line_num in EXTRA_SKIP:
        return False
    # Structural markers are not headings
    if PAGE_RE.match(s):
        return False
    if NS_MARKER_RE.match(s):
        return False
    if s.startswith('<'):
        return False
    if COLOPHON_RE.match(s):
        return False
    if SEPARATOR_RE.match(s):
        return False
    if SUTRA_RE.search(s):
        return False
    # Headings don't end with sentence/verse markers
    if SENT_END_RE.search(s):
        return False
    # Headings don't contain mid-sentence `।`
    if '।' in s:
        return False
    # Headings don't contain `॥`
    if '॥' in s:
        return False
    # Must start with Devanagari
    if not re.match(r'^[ँ-ॿ]', s):
        return False
    return True


def classify_line(s, line_num, in_av):
    """Return the type of this line."""
    if not s:
        return 'empty'
    if PAGE_RE.match(s):
        return 'page'
    if NS_MARKER_RE.match(s):
        return 'ns_marker'
    if COLOPHON_RE.match(s):
        return 'colophon'
    if SEPARATOR_RE.match(s):
        return 'separator'
    if SUTRA_RE.search(s):
        return 'sutra'
    if s.startswith('<'):
        return 'av_start'
    if in_av:
        return 'av_cont'
    if line_num in HEADING_LINES:
        return 'heading'
    return 'commentary'


def parse_file(filepath):
    """Parse the file into topic groups."""
    with open(filepath, 'r', encoding='utf-8') as f:
        raw_lines = f.readlines()

    topics = []
    current = None
    in_av = False
    preamble_lines = []  # Lines before the first heading
    sutra_line = None

    for i, raw in enumerate(raw_lines, 1):
        s = raw.rstrip('\n').strip()

        # Track AV block state
        if s.startswith('<'):
            in_av = True
            if current:
                current['av'].append(s)
            else:
                preamble_lines.append(('av', s))
            if AV_END_RE.search(s):
                in_av = False
            continue

        if in_av:
            if current:
                current['av'].append(s)
            if AV_END_RE.search(s):
                in_av = False
            continue

        # Classify
        kind = classify_line(s, i, in_av)

        if kind in ('empty', 'page', 'ns_marker', 'separator'):
            continue
        if kind == 'colophon':
            if current:
                current['colophon'] = s
            continue
        if kind == 'sutra':
            sutra_line = s
            continue

        if kind == 'heading':
            current = {
                'heading': s,
                'line': i,
                'commentary': [],
                'av': [],
                'colophon': None,
            }
            topics.append(current)
            continue

        # av_start handled above; commentary
        if kind == 'commentary':
            if current:
                current['commentary'].append(s)
            else:
                preamble_lines.append(('text', s))

    return topics, preamble_lines, sutra_line


def detect_missing_headings(filepath):
    """Detect potential headings not in HEADING_LINES set."""
    with open(filepath, 'r', encoding='utf-8') as f:
        raw_lines = f.readlines()

    in_av = False
    candidates = []

    for i, raw in enumerate(raw_lines, 1):
        s = raw.rstrip('\n').strip()
        if not s:
            continue

        if s.startswith('<'):
            in_av = True
            if AV_END_RE.search(s):
                in_av = False
            continue
        if in_av:
            if AV_END_RE.search(s):
                in_av = False
            continue

        if i in HEADING_LINES:
            continue  # Already known

        if is_heading_heuristic(s, i, in_av):
            candidates.append((i, s))

    return candidates


def format_av_box(av_lines):
    """Format AV verses as a markdown table box."""
    if not av_lines:
        return ''
    # Clean AV lines: remove < > brackets
    cleaned = []
    for line in av_lines:
        line = line.strip()
        if line.startswith('<'):
            line = line[1:]
        if line.endswith('>'):
            line = line[:-1]
        line = line.strip()
        if line:
            cleaned.append(line)
    if not cleaned:
        return ''
    lines_out = []
    lines_out.append('')
    lines_out.append('| **अनुव्याख्यानम् (AV):** |')
    lines_out.append('|:---|')
    for cl in cleaned:
        # Escape pipe characters in content
        cl_escaped = cl.replace('|', '\\|')
        lines_out.append(f'| {cl_escaped} |')
    lines_out.append('')
    return '\n'.join(lines_out)


def format_samiksha_box():
    """Format empty Samīkṣā box as markdown table."""
    lines = []
    lines.append('')
    lines.append('| **समीक्षा (Samīkṣā) — Author\'s Review:** |')
    lines.append('|:---|')
    for _ in range(5):
        lines.append('| &nbsp; |')
    lines.append('')
    return '\n'.join(lines)


def build_output(topics):
    """Build the reorganized markdown output."""
    out = []

    # Header
    out.append('# न्यायसुधा — जिज्ञासाधिकरणम् एवं जन्माधिकरणम्')
    out.append('')
    out.append('**ग्रन्थकारः** — जयतीर्थः')
    out.append('')
    out.append('**Source** — Nyāya Sudhā on Brahma Sūtra 1.1.1–1.1.2')
    out.append('')
    out.append('---')
    out.append('')

    # Split topics into Jijñāsā and Janmā
    jijnasa = [t for t in topics if t['line'] < JANMA_START]
    janma   = [t for t in topics if t['line'] >= JANMA_START]

    # ── Section 1: Jijñāsādhikaraṇa ──
    out.append('# भाग १ — जिज्ञासाधिकरणम् (ब्रह्मसूत्र १.१.१)')
    out.append('')

    for idx, topic in enumerate(jijnasa, 1):
        out.append(f'# {idx}. {topic["heading"]}')
        out.append('')

        # Commentary points
        if topic['commentary']:
            out.append('## न्यायसुधा')
            out.append('')
            for pidx, point in enumerate(topic['commentary'], 1):
                out.append(f'{idx}.{pidx} {point}')
                out.append('')

        # AV box
        av_box = format_av_box(topic['av'])
        if av_box:
            out.append(av_box)

        # Samīkṣā box
        out.append(format_samiksha_box())

        out.append('---')
        out.append('')

    # ── Section 2: Janmādhikaraṇa ──
    out.append('')
    out.append('# भाग २ — जन्माधिकरणम् (ब्रह्मसूत्र १.१.२)')
    out.append('')

    for idx, topic in enumerate(janma, 1):
        out.append(f'# {idx}. {topic["heading"]}')
        out.append('')

        # Commentary points
        if topic['commentary']:
            out.append('## न्यायसुधा')
            out.append('')
            for pidx, point in enumerate(topic['commentary'], 1):
                out.append(f'{idx}.{pidx} {point}')
                out.append('')

        # AV box
        av_box = format_av_box(topic['av'])
        if av_box:
            out.append(av_box)

        # Samīkṣā box
        out.append(format_samiksha_box())

        out.append('---')
        out.append('')

    # Closing
    out.append('॥ इति श्रीमन्न्यायसुधायां जिज्ञासाधिकरणजन्माधिकरणे समाप्तम् ॥')
    out.append('')

    return '\n'.join(out)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'reorganize'

    if mode == 'detect':
        # Show potential missed headings
        candidates = detect_missing_headings(INPUT)
        print(f'Found {len(candidates)} candidate headings NOT in HEADING_LINES:')
        print()
        for ln, text in candidates:
            flag = '  [JANMA]' if ln >= JANMA_START else ''
            print(f'  {ln:5d}: {text[:80]}{flag}')
        print()
        print(f'Current HEADING_LINES has {len(HEADING_LINES)} entries.')
        return

    if mode == 'reorganize':
        # First detect potential issues
        candidates = detect_missing_headings(INPUT)
        if candidates:
            print(f'Note: {len(candidates)} potential headings detected outside HEADING_LINES.')
            print('Run with "detect" argument to review them.')
            print()

        topics, preamble, sutra = parse_file(INPUT)

        # Stats
        jijnasa = [t for t in topics if t['line'] < JANMA_START]
        janma   = [t for t in topics if t['line'] >= JANMA_START]
        total_points = sum(len(t['commentary']) for t in topics)
        total_av = sum(len(t['av']) for t in topics)

        print(f'Parsed {len(topics)} topics:')
        print(f'  Jijñāsā: {len(jijnasa)} topics')
        print(f'  Janmā:   {len(janma)} topics')
        print(f'  Total commentary points: {total_points}')
        print(f'  Total AV verse lines: {total_av}')
        print()

        output = build_output(topics)

        with open(OUTPUT, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f'Written reorganized file to: {OUTPUT}')

        # Print TOC
        print()
        print('TABLE OF CONTENTS:')
        print('=' * 60)
        print()
        print('भाग १ — जिज्ञासाधिकरणम्')
        for i, t in enumerate(jijnasa, 1):
            print(f'  {i:3d}. {t["heading"][:60]}')
        print()
        print('भाग २ — जन्माधिकरणम्')
        for i, t in enumerate(janma, 1):
            print(f'  {i:3d}. {t["heading"][:60]}')


if __name__ == '__main__':
    main()
