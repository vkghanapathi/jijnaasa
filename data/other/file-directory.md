# Jijñāsā Adhikaraṇa — File Directory

## Dvaita Side (`data/dvaita/`)

| # | File | Size | Description |
|---|------|------|-------------|
| 1 | `02-bs-ns12.docx` | 140KB | Reorganized Nyāya Sudhā source text (89 episodes) |
| 2 | `02-bs-ns12.md` | — | Markdown source of the above |
| 3 | `03-ns-analysis.docx` | 105KB | English episode-wise Pūrvapakṣa-Siddhānta analysis |
| 4 | `05-ns-review.docx` | 80KB | Sanskrit analysis (89 episodes, Devanagari) |
| 5 | `05-ns-review.md` | 237KB | Sanskrit analysis (Markdown reference) |

### Source/Intermediate

| # | File | Description |
|---|------|-------------|
| 6 | `sanskrit_eps_01_22.md` | Sanskrit translation batch 1 (Episodes 1–22) |
| 7 | `sanskrit_eps_23_44.md` | Sanskrit translation batch 2 (Episodes 23–44) |
| 8 | `sanskrit_eps_45_66.md` | Sanskrit translation batch 3 (Episodes 45–66) |
| 9 | `sanskrit_eps_67_end.md` | Sanskrit translation batch 4 (Episodes 67–89 + Janmādhi. 1–6) |
| 10 | `ns-analysis.md` | English analysis (Markdown reference) |

### Scripts

| # | File | Description |
|---|------|-------------|
| 11 | `reorganize_ns.py` | VKG-VyP reorganization of Nyāya Sudhā |
| 12 | `fix_numbering.py` | Fix numbering + generate TOC + docx |
| 13 | `compile_analysis.py` | Compiled agent outputs → ns-analysis |
| 14 | `compile_sanskrit.py` | Compiled Sanskrit batches → 05-ns-review |

---

## Advaita Side (`data/advaita/`)

| # | File | Size | Description |
|---|------|------|-------------|
| 1 | `04-dn-episodes.docx` | 63KB | Dhvānta Nirāsa episode breakdown (46 episodes) |
| 2 | `04-dn-episodes.md` | 135KB | DN episodes (Markdown reference) |
| 3 | `Dhvantanirasa_Final.md` | 355KB | Dhvānta Nirāsa original source text |
| 4 | `bs12-as.md` | 33KB | Śaṅkara Bhāṣya digital text (BS 1.1.1–1.1.2) |
| 5 | `plan1.md` | — | Thesis outline |
| 6 | `Ananda Giri Teeka.pdf` | 1.8MB | Ānandagiri Ṭīkā (scanned, 31 pages) |

### Source/Intermediate

| # | File | Description |
|---|------|-------------|
| 7 | `dn-episodes-jijnasa.md` | DN Jijñāsā section (28 episodes) |
| 8 | `dn-episodes-janmadya.md` | DN Janmādya + Śāstrayonitva + Samanvaya (18 episodes) |

### Scripts

| # | File | Description |
|---|------|-------------|
| 9 | `compile_dn.py` | Compiled DN episode files → 04-dn-episodes |

---

## Other (`data/other/`)

| # | File | Description |
|---|------|-------------|
| 1 | `file-directory.md` | This file |

---

## Pipeline Status

- [x] Stage 02 — Nyāya Sudhā reorganization (`02-bs-ns12`)
- [x] Stage 03 — English episode analysis (`03-ns-analysis`)
- [x] Stage 04 — Dhvānta Nirāsa episode compilation (`04-dn-episodes`)
- [x] Stage 05 — Sanskrit analysis (`05-ns-review`)
- [ ] Port original NS text into analysis episodes
- [ ] Telugu combined document (`03-ns-tl.docx`)
