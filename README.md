# The World in One Day — Tuesday 24 November 2026

Entry for make.fun competition **news-image-20261124**:
"Sum up 24 November's world news in one image".

## What it is

`main.py` (Python 3.13, Pillow only, no network, no external files) draws
one 1024×1024 PNG frontpage entirely in code — flat vector-style scenes,
a simplified world map, and text. Running it writes:

- `./entry.png` (next to this file, for local testing)
- `/output/entry.png` (when `/output` exists, as the bounty harness expects)

## Content

- **35 dated stories, 8 regions, 14 fields** — every story is dated
  Tuesday 24 November 2026 (UTC), numbered 1–35, with a status pill
  (CONFIRMED / OFFICIAL / REPORTED / CLAIM) and a short source.
- **Heroes 1–3:** Hormuz — 3 tankers hit (mine claim labelled CLAIM,
  UNCONFIRMED); Riyadh PIF Tower hit, 11 hurt; Nvidia +30%, Nasdaq +6.51%.
  Each hero has a LARGE flat vector scene (tankers + flames, PIF tower +
  drone, rising bars + arrow) and a red stat banner.
- **Grid 4–13** (5×2, cards 128 px tall), each with a big flat mini-scene
  + stat chip, **map** with numbered pins 1–13 (all ≥28.3 px apart, short
  leader lines to true spots; NO Europe inset, NO dotted map),
  **22 one-line briefs 14–35**, **one-line UTC timeline** (6 items, honest
  times only — no PRESS TIME claim; the Hormuz 20:25* is explained in
  DATE CHECK as 20:25 UTC 23 Nov), **DATE CHECK** box listing what was
  deliberately excluded (COP31 ended 22 Nov, ICJ ruling 19 Nov, Nvidia
  CEO restored 23 Nov, Shenzhou-24 launch 25 Nov, Hormuz 20:25 UTC 23 Nov)
  and what had not happened yet (Cartagena rescue 25 Nov, Houthi claim
  25 Nov, Australia–Solomons deal 25 Nov), plus a HOW SURE legend and
  full source list in the footer. All body text is ≥10 px.

## Run & verify

```bash
python3 main.py
# writes entry.png (1024x1024, ~225 KB) and /output/entry.png
```

Deterministic: two runs produce byte-identical output
(SHA256 `7d203750b025e51d40b9242f978774eee3e0183209d8d06b0085dc1e557300cf`,
225,258 bytes, verified 2026-11-26, v6 rebuild).
v3 (206,972 bytes) was submitted and passed checks; v4 (213,291 bytes,
score 95), v5 (228,342 bytes, score 96) and v6 (225,258 bytes, score 96)
are held backups — do not submit until nemesis confirms.
v6 rebuild (per nemesis: "gambar peta gk jelas gambar newsnya juga
kayak apa itu, lihat referensi top rank news sebelumnya"): read the
rank-1 images visually (regian 23 Nov, bagarte 22 Nov, superskie 21 Nov)
and rebuilt from scratch in their flat frontpage style — big simple hero
scenes, big flat grid icons + stat chips, small simple solid map with
large separated pins and no Europe inset, one-line UTC timeline with no
PRESS TIME claim, all body text ≥10 px, and the v5 submission title
naming the three headlines.

## Sources

Research: `../bounty-news/news24-research.md` (37 stories from the 17
listed news sources, cross-checked against primary/official sources).
Design pattern: `../bounty-news/winner-analysis.md` (top-10 analysis of
news-image 20261120–23 winners; structure and discipline imitated,
content is all 24 Nov).

## License

MIT — see `LICENSE`.
