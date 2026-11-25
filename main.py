#!/usr/bin/env python3
"""news-image-20261124: Tuesday 24 November 2026 world frontpage (v6).

Rebuilt from scratch after nemesis said v5 was ugly, stiff, and its map
unclear. v6 copies the STRUCTURE of the rank-1 winners (regian 23 Nov,
bagarte 22 Nov, superskie 21 Nov), not their content:

- flat frontpage, no drop shadows, no heavy rounding, no tint washes;
- giant serif date, red 3-story subheadline, coloured region strip,
  one-line UTC timeline strip (no PRESS TIME claim);
- 3 heroes with LARGE, simple, flat vector scenes + red stat banners;
- grid 5x2 with big flat mini-scenes + stat chips, white cards;
- small, simple, solid world map with LARGE numbered pins (>=26 px
  apart, leader lines where a pin is moved off its true spot) and a
  colour legend. No Europe inset, no dotted map, no tiny pins.

Draws ONE 1024x1024 PNG entirely in code (Pillow vector-style shapes +
text). No network, no photos, no external files, fully deterministic:
running it twice produces byte-identical output.
Writes /output/entry.png when /output exists, and ./entry.png next to
this file. Python 3.13 / Pillow.

Facts, dates and numbers are the same 35 stories as v3-v5 (see
news24-research.md); the same date traps are obeyed.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 242, 230)
PANEL = (255, 253, 246)
NAVY = (22, 35, 63)
RED = (179, 39, 30)
GOLD = (201, 162, 39)
INK = (26, 26, 26)
GREY = (90, 90, 86)
RULE = (200, 192, 172)
OCEAN = (220, 233, 242)
LAND = (217, 201, 163)
LAND_LINE = (150, 138, 110)

REGION_COLORS = {
    "N. AMERICA": (31, 78, 121),
    "S. AMERICA": (176, 48, 96),
    "EUROPE": (37, 99, 168),
    "MIDDLE EAST": (217, 115, 26),
    "AFRICA": (124, 58, 237),
    "S. ASIA": (46, 125, 50),
    "E. ASIA & PACIFIC": (14, 124, 123),
    "GLOBAL": (91, 107, 122),
}

STATUS_FILL = {
    "CONFIRMED": (31, 78, 121),
    "OFFICIAL": (46, 125, 50),
    "REPORTED": (217, 115, 26),
    "CLAIM": (179, 39, 30),
}

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def tint(color, frac=0.90):
    """Mix a region colour with white for a pale scene background."""
    return tuple(int(color[i] * (1 - frac) + 255 * frac) for i in range(3))


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def pill(draw, xy, text, fnt, bg, fg=(255, 255, 255)):
    x, y = xy
    w_ = draw.textlength(text, font=fnt) + 10
    h_ = fnt.size + 6
    draw.rounded_rectangle([x, y, x + w_, y + h_], radius=3, fill=bg)
    draw.text((x + 5, y + 3), text, font=fnt, fill=fg)
    return w_


def star(draw, cx, cy, r_out, r_in, n, fill):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = -math.pi / 2 + i * math.pi / n
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


# ---------------------------------------------------------------- stories
# heroes: n, region, headline, deck, status, source, stat, kind
HEROES = [
    (1, "MIDDLE EAST",
     "HORMUZ: 3 TANKERS HIT",
     "Three tankers hit by unknown projectiles in the Strait; crews safe. "
     "Mine claim UNCONFIRMED.",
     "CLAIM", "Al Jazeera / Reuters / UKMTO",
     "3 TANKERS HIT", "ship"),
    (2, "MIDDLE EAST",
     "RIYADH TOWER HIT, 11 HURT",
     "Drone hits the 80-storey PIF Tower, 2nd strike in a week; "
     "coalition blames a Houthi drone.",
     "CONFIRMED", "Reuters / Al Jazeera / SPA",
     "11 HURT", "tower"),
    (3, "N. AMERICA",
     "NVIDIA +30% AS MARKETS SOAR",
     "Nvidia +30% as Huang returned; Nasdaq +6.51%, S&P +4.73%. Huawei guilty 10/12.",
     "CONFIRMED", "BBC / Reuters / AP",
     "NASDAQ +6.51%", "chart"),
]

# grid: n, region, headline, deck, status, source, kind, stat, stat_bg
GRID = [
    (4, "S. AMERICA", "CARTAGENA SIEGE: 25-30 HOSTAGES",
     "Gunmen seized shoppers at an Exito store; 10 freed 24 Nov.",
     "CONFIRMED", "AP / Reuters", "hostage", "25-30 HELD", RED),
    (5, "N. AMERICA", "HUAWEI GUILTY ON 10 OF 12 COUNTS",
     "NY jury convicts Huawei: theft, fraud, sanctions breaches.",
     "CONFIRMED", "AJ / AP / BBC", "court", "10 OF 12", NAVY),
    (6, "EUROPE", "ZAPORIZHZHIA: 2 DEAD, 30+ HURT",
     "Night strike kills 2, wounds 30+, incl. 4 children, a baby.",
     "CONFIRMED", "Reuters / AP", "blast", "2 DEAD · 30+ HURT", RED),
    (7, "E. ASIA & PACIFIC", "ICJ RULING BACKED BY 14 NATIONS",
     "Britain, Spain, Canada, Australia + 10 back the Rohingya ruling.",
     "CONFIRMED", "BBC / Reuters", "doc", "14 NATIONS", NAVY),
    (8, "AFRICA", "SENEGAL'S AFCON TITLE RESTORED",
     "CAS overturns CAF ruling; Senegal champions again, 1-0.",
     "OFFICIAL", "AP / NPR / CAS", "trophy", "SENEGAL 1-0", NAVY),
    (9, "EUROPE", "EU SANCTIONS: 60 BANKS, 70 SHIPS",
     "EU proposes curbs: 60 banks, 70 shadow tankers, crypto.",
     "OFFICIAL", "Reuters / Politico", "euflag", "60 BANKS · 70 SHIPS", NAVY),
    (10, "MIDDLE EAST", "GAZA: >99% CONTAMINATED",
     "Oxfam: contamination signs in >99% of Gaza; 7 killed.",
     "REPORTED", "Oxfam / Al Jazeera", "warn", ">99%", RED),
    (11, "S. ASIA", "NEPAL QUAKE M5.6 / M5.3, NO DEAD",
     "Quake near Taplejung at 01:32 UTC; M5.6 vs M5.3, no deaths.",
     "CONFIRMED", "NEMRC / USGS", "quake", "M5.6 / M5.3", NAVY),
    (12, "E. ASIA & PACIFIC", "SHENZHOU-24 CREW NAMED",
     "China names Tang Hongbo, Wu Yi, Zeeshan Ali. Launch 25 Nov.",
     "OFFICIAL", "Xinhua / Reuters", "rocket", "CREW NAMED", NAVY),
    (13, "EUROPE", "MI5 WARNS OF RUSSIAN SABOTAGE",
     "MI5, NPSA, MoD warn Ukraine suppliers of Russian sabotage.",
     "OFFICIAL", "MI5 / NPSA / BBC", "shield", "WARNING", NAVY),
]

BRIEFS = [
    (14, "N. AMERICA", "DOJ recovers $8bn, charges 800+ in scam sweep.", "DOJ"),
    (15, "N. AMERICA", "Abrego Garcia leaves US voluntarily for Spain.", "NPR / AP"),
    (16, "N. AMERICA", "Pennsylvania: 9th measles death; 46 counties.", "CDC / PA"),
    (17, "S. AMERICA", "Villavicencio bomb wrecks building; no deaths.", "Pres."),
    (18, "S. AMERICA", "Venezuela discloses $237.5bn public debt.", "Reuters"),
    (19, "S. AMERICA", "Mexico will try 'El Chapo Isidro' at home.", "AP"),
    (20, "EUROPE", "NATO sends AWACS to Poland after 3 missiles fell.", "NATO"),
    (21, "EUROPE", "Spain split before vote; far right may govern.", "BBC"),
    (22, "EUROPE", "Macron pushes minerals reserve, budget rule.", "Élysée"),
    (23, "MIDDLE EAST", "Iran: no talks till US meets 7 conditions.", "Al Jazeera"),
    (24, "MIDDLE EAST", "Yemen: Saudi strikes reported; toll unproven.", "Houthi"),
    (25, "MIDDLE EAST", "Ahmadi given 74 lashes for unveiled concert.", "Al Jazeera"),
    (26, "MIDDLE EAST", "Libya asks Kyiv to explain Benghazi strike.", "Reuters"),
    (27, "AFRICA", "Sudan army: RSF drone hit a UN building.", "Army claim"),
    (28, "AFRICA", "Ethiopia, Eritrea face off again at Badme.", "JA"),
    (29, "AFRICA", "Borno enrolment nearly doubles despite war.", "Al Jazeera"),
    (30, "S. ASIA", "Hasina plans return 16 Dec despite sentence.", "BBC"),
    (31, "E. ASIA & PACIFIC", "Solomons ends China pact; turns to Australia.", "Reuters"),
    (32, "E. ASIA & PACIFIC", "S. Korea scrambles jets over Russian ADIZ entry.", "Yonhap"),
    (33, "E. ASIA & PACIFIC", "Malaysia to repatriate 6,500+ Myanmar nationals.", "AP"),
    (34, "GLOBAL", "Guterres seeks AI-risk framework within a year.", "UN"),
    (35, "GLOBAL", "UN 'disappointed' by COP31; COP32 to Addis.", "UN"),
]

# One-line UTC strip: only times the research actually gives. The Hormuz
# incident is 20:25 UTC on 23 Nov, first reported 24 Nov (see DATE CHECK).
TIMELINE = [
    ("01:32", "Nepal quake"),
    ("Morning", "MI5 warning"),
    ("Midday", "Nasdaq +6.51%"),
    ("Afternoon", "Huawei guilty"),
    ("Evening", "Riyadh hit"),
    ("20:25*", "Hormuz reported"),
]

REGIONS_STRIP = [
    ("N. AMERICA", 5), ("S. AMERICA", 4), ("EUROPE", 6),
    ("MIDDLE EAST", 7), ("AFRICA", 4), ("S. ASIA", 2),
    ("E. ASIA & PACIFIC", 5), ("GLOBAL", 2),
]

# ---------------------------------------------------------------- scenes
# Hero scenes are drawn LARGE and simple: a few flat shapes that read in
# one second (tanker hulls + flames, tower + drone, rising bars + arrow).

def draw_hero_scene(draw, box, kind):
    x0, y0, x1, y1 = box
    w_, h_ = x1 - x0, y1 - y0
    cx = (x0 + x1) // 2
    if kind == "ship":
        draw.rectangle(box, fill=(214, 231, 238))
        # sun + clouds
        draw.ellipse([x0 + 18, y0 + 8, x0 + 46, y0 + 36], fill=(255, 214, 120))
        draw.ellipse([x0 + 210, y0 + 12, x0 + 252, y0 + 26], fill=(255, 255, 255))
        draw.ellipse([x0 + 232, y0 + 6, x0 + 268, y0 + 20], fill=(255, 255, 255))
        # sea
        draw.rectangle([x0, y0 + 58, x1, y1], fill=(158, 198, 222))
        for wy in (y0 + 70, y0 + 84, y0 + 96):
            draw.line([x0 + 8, wy, x1 - 8, wy], fill=(255, 255, 255), width=2)
        # background tanker (small, far)
        draw.rectangle([x0 + 96, y0 + 34, x0 + 210, y0 + 48], fill=(90, 107, 122))
        draw.rectangle([x0 + 140, y0 + 26, x0 + 168, y0 + 34], fill=(90, 107, 122))
        # flames above the middle tanker
        draw.polygon([(x0 + 128, y0 + 34), (x0 + 142, y0 + 8), (x0 + 152, y0 + 30),
                      (x0 + 164, y0 + 6), (x0 + 176, y0 + 34)], fill=(217, 115, 26))
        draw.polygon([(x0 + 140, y0 + 34), (x0 + 150, y0 + 18), (x0 + 162, y0 + 34)],
                     fill=(255, 204, 0))
        # foreground tanker, left
        draw.rectangle([x0 + 8, y0 + 62, x0 + 138, y0 + 80], fill=NAVY)
        draw.rectangle([x0 + 30, y0 + 50, x0 + 78, y0 + 62], fill=(255, 253, 246))
        draw.rectangle([x0 + 88, y0 + 46, x0 + 104, y0 + 62], fill=RED)
        # foreground tanker, right
        draw.rectangle([x0 + 168, y0 + 68, x0 + 298, y0 + 86], fill=NAVY)
        draw.rectangle([x0 + 196, y0 + 56, x0 + 244, y0 + 68], fill=(255, 253, 246))
        draw.rectangle([x0 + 254, y0 + 52, x0 + 270, y0 + 68], fill=RED)
    elif kind == "tower":
        draw.rectangle(box, fill=(250, 233, 203))
        draw.ellipse([x0 + 14, y0 + 8, x0 + 42, y0 + 36], fill=(255, 214, 120))
        # ground
        draw.rectangle([x0, y1 - 12, x1, y1], fill=(198, 186, 158))
        # skyline, low blocks either side
        draw.rectangle([x0 + 6, y0 + 66, x0 + 52, y1 - 12], fill=(120, 128, 140))
        draw.rectangle([x0 + 58, y0 + 80, x0 + 92, y1 - 12], fill=(150, 156, 166))
        draw.rectangle([x0 + 226, y0 + 62, x0 + 268, y1 - 12], fill=(120, 128, 140))
        draw.rectangle([x0 + 272, y0 + 78, x0 + 300, y1 - 12], fill=(150, 156, 166))
        # PIF tower: tall stepped navy tower, centre
        draw.polygon([(cx - 24, y1 - 12), (cx - 15, y0 + 6), (cx + 15, y0 + 6),
                      (cx + 24, y1 - 12)], fill=NAVY)
        for i in range(6):
            yy = y0 + 20 + i * 13
            draw.line([cx - 17, yy, cx + 17, yy], fill=(255, 210, 100), width=2)
        draw.ellipse([cx - 4, y0 + 2, cx + 4, y0 + 10], fill=RED)
        # impact burst on the tower
        star(draw, cx + 27, y0 + 52, 14, 6, 8, (217, 115, 26))
        star(draw, cx + 27, y0 + 52, 7, 3, 8, (255, 204, 0))
        # drone, upper right
        dx, dy = x0 + 238, y0 + 20
        draw.rectangle([dx, dy, dx + 16, dy + 6], fill=INK)
        draw.line([dx - 6, dy - 2, dx + 22, dy - 2], fill=INK, width=2)
        draw.ellipse([dx - 10, dy - 6, dx - 2, dy + 2], fill=INK)
        draw.ellipse([dx + 18, dy - 6, dx + 26, dy + 2], fill=INK)
        draw.line([dx + 8, dy + 6, dx + 8, dy + 12], fill=INK, width=2)
    elif kind == "chart":
        draw.rectangle(box, fill=(216, 238, 222))
        # faint grid lines
        for gy in (y0 + 22, y0 + 46, y0 + 70):
            draw.line([x0 + 14, gy, x1 - 14, gy], fill=(190, 210, 196), width=1)
        # axes
        draw.line([x0 + 16, y0 + 10, x0 + 16, y1 - 12], fill=NAVY, width=3)
        draw.line([x0 + 16, y1 - 12, x1 - 10, y1 - 12], fill=NAVY, width=3)
        # four big rising bars
        bw, gap = 46, 18
        for i, hh in enumerate((26, 46, 66, 88)):
            bx0 = x0 + 30 + i * (bw + gap)
            draw.rectangle([bx0, y1 - 12 - hh, bx0 + bw, y1 - 12],
                           fill=((37, 99, 168), (31, 78, 121),
                                 (46, 125, 50), (22, 35, 63))[i])
        # rising arrow over the bars
        pts = [(x0 + 34, y1 - 34), (x0 + 98, y1 - 52), (x0 + 162, y1 - 72),
               (x0 + 226, y1 - 92), (x0 + 282, y1 - 100)]
        draw.line(pts, fill=(46, 125, 50), width=5)
        draw.polygon([(x0 + 282, y1 - 100), (x0 + 262, y1 - 100),
                      (x0 + 276, y1 - 84)], fill=(46, 125, 50))


def draw_grid_icon(draw, box, kind, color):
    """One big flat glyph, box-relative so it scales with the scene."""
    x0, y0, x1, y1 = box
    w_, h_ = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    u = min(w_, h_) / 40.0 * 1.25  # unit: scene is ~36 units tall
    if kind == "hostage":  # storefront, striped awning + door
        for i in range(4):
            fill = RED if i % 2 == 0 else (255, 253, 246)
            draw.rectangle([cx - 16 * u + i * 8 * u, y0 + 4 * u,
                            cx - 8 * u + i * 8 * u, y0 + 11 * u], fill=fill)
        draw.rectangle([cx - 16 * u, y0 + 11 * u, cx + 16 * u, y1 - 4 * u], fill=NAVY)
        for r in range(2):
            for c in range(3):
                draw.rectangle([cx - 13 * u + c * 10 * u, y0 + 15 * u + r * 10 * u,
                                cx - 6 * u + c * 10 * u, y0 + 21 * u + r * 10 * u],
                               fill=(255, 253, 246))
        draw.rectangle([cx - 3 * u, y1 - 12 * u, cx + 3 * u, y1 - 4 * u], fill=RED)
    elif kind == "court":  # scales of justice
        draw.line([cx, y0 + 4 * u, cx, y1 - 6 * u], fill=NAVY, width=3)
        draw.line([cx - 15 * u, y0 + 8 * u, cx + 15 * u, y0 + 8 * u], fill=NAVY, width=3)
        draw.polygon([(cx - 19 * u, y0 + 14 * u), (cx - 11 * u, y0 + 14 * u),
                      (cx - 15 * u, y0 + 24 * u)], fill=NAVY)
        draw.polygon([(cx + 11 * u, y0 + 14 * u), (cx + 19 * u, y0 + 14 * u),
                      (cx + 15 * u, y0 + 24 * u)], fill=NAVY)
        draw.rectangle([cx - 8 * u, y1 - 6 * u, cx + 8 * u, y1 - 3 * u], fill=NAVY)
    elif kind == "blast":  # explosion starburst
        star(draw, cx, cy, 14 * u, 6 * u, 8, (217, 115, 26))
        star(draw, cx, cy, 8 * u, 3.5 * u, 8, RED)
        draw.ellipse([cx - 4 * u, cy - 4 * u, cx + 4 * u, cy + 4 * u], fill=(255, 204, 0))
    elif kind == "doc":  # court document with red seal
        draw.rectangle([cx - 11 * u, y0 + 3 * u, cx + 11 * u, y1 - 3 * u],
                       fill=(255, 253, 246), outline=NAVY, width=2)
        draw.polygon([(cx + 4 * u, y0 + 3 * u), (cx + 11 * u, y0 + 10 * u),
                      (cx + 4 * u, y0 + 10 * u)], fill=(200, 192, 172))
        for yy in (y0 + 8 * u, y0 + 13 * u, y0 + 18 * u):
            draw.line([cx - 8 * u, yy, cx + 6 * u, yy], fill=NAVY, width=2)
        draw.ellipse([cx + 1 * u, y1 - 12 * u, cx + 10 * u, y1 - 3 * u], fill=RED)
    elif kind == "trophy":
        draw.polygon([(cx - 8 * u, y0 + 3 * u), (cx + 8 * u, y0 + 3 * u),
                      (cx + 6 * u, y0 + 16 * u), (cx - 6 * u, y0 + 16 * u)],
                     fill=(217, 115, 26))
        draw.arc([cx - 15 * u, y0 + 3 * u, cx - 5 * u, y0 + 14 * u], 90, 270,
                 fill=(217, 115, 26), width=3)
        draw.arc([cx + 5 * u, y0 + 3 * u, cx + 15 * u, y0 + 14 * u], 270, 90,
                 fill=(217, 115, 26), width=3)
        draw.rectangle([cx - 3 * u, y0 + 16 * u, cx + 3 * u, y0 + 24 * u], fill=NAVY)
        draw.rectangle([cx - 10 * u, y0 + 24 * u, cx + 10 * u, y0 + 28 * u], fill=NAVY)
    elif kind == "euflag":  # EU flag, navy field, 12 gold stars
        draw.rectangle([cx - 19 * u, y0 + 4 * u, cx + 19 * u, y1 - 4 * u], fill=(0, 51, 153))
        for k in range(12):
            a = k * math.pi / 6 - math.pi / 2
            sx = cx + 11 * u * math.cos(a)
            sy = cy + 8 * u * math.sin(a)
            draw.ellipse([sx - 1.6 * u, sy - 1.6 * u, sx + 1.6 * u, sy + 1.6 * u],
                         fill=(255, 204, 0))
    elif kind == "warn":  # amber warning triangle
        draw.polygon([(cx, y0 + 2 * u), (cx + 15 * u, y1 - 3 * u),
                      (cx - 15 * u, y1 - 3 * u)], fill=(217, 115, 26), outline=NAVY)
        draw.text((cx, y0 + 12 * u), "!", font=font(SANS_B, 16), fill=(255, 255, 255),
                  anchor="ma")
    elif kind == "quake":  # seismograph zigzag
        pts = [(x0 + 6 * u, y1 - 12 * u), (x0 + 14 * u, y0 + 8 * u),
               (x0 + 22 * u, y1 - 18 * u), (x0 + 30 * u, y0 + 10 * u),
               (x0 + 38 * u, y1 - 12 * u)]
        draw.line(pts, fill=RED, width=4)
        draw.line([x0 + 4 * u, y1 - 6 * u, x1 - 4 * u, y1 - 6 * u], fill=NAVY, width=2)
    elif kind == "rocket":
        draw.polygon([(cx, y0 + 2 * u), (cx + 8 * u, y0 + 18 * u),
                      (cx + 5 * u, y1 - 14 * u), (cx - 5 * u, y1 - 14 * u),
                      (cx - 8 * u, y0 + 18 * u)], fill=NAVY)
        draw.ellipse([cx - 3 * u, y0 + 12 * u, cx + 3 * u, y0 + 18 * u],
                     fill=(255, 253, 246))
        draw.polygon([(cx - 5 * u, y1 - 14 * u), (cx - 11 * u, y1 - 4 * u),
                      (cx - 2 * u, y1 - 10 * u)], fill=RED)
        draw.polygon([(cx + 5 * u, y1 - 14 * u), (cx + 11 * u, y1 - 4 * u),
                      (cx + 2 * u, y1 - 10 * u)], fill=RED)
    elif kind == "shield":
        draw.polygon([(cx, y0 + 3 * u), (cx + 14 * u, y0 + 9 * u),
                      (cx + 14 * u, y0 + 22 * u), (cx, y1 - 3 * u),
                      (cx - 14 * u, y0 + 22 * u), (cx - 14 * u, y0 + 9 * u)], fill=NAVY)
        draw.text((cx, y0 + 11 * u), "!", font=font(SANS_B, 16), fill=(255, 255, 255),
                  anchor="ma")


# ---------------------------------------------------------------- cards

def draw_hero(draw, x, y, w_, h_, story):
    n, region, headline, deck, status, source, stat, kind = story
    color = REGION_COLORS[region]
    draw.rectangle([x, y, x + w_, y + h_], fill=PANEL, outline=color, width=2)
    # header: number + place, pill at right
    draw.text((x + 10, y + 6), f"{n}", font=font(SANS_B, 14), fill=color)
    draw.text((x + 30, y + 8), region, font=font(SANS_B, 11), fill=NAVY)
    pw = pill(draw, (x + w_ - 8 - (draw.textlength(status, font=font(SANS_B, 10)) + 10),
                     y + 5), status, font(SANS_B, 10), STATUS_FILL[status])
    # LARGE flat scene
    draw_hero_scene(draw, (x + 1, y + 28, x + w_ - 1, y + 128), kind)
    # red stat banner
    draw.rectangle([x + 1, y + 128, x + w_ - 1, y + 160], fill=RED)
    draw.text((x + w_ // 2, y + 134), stat, font=font(SANS_B, 20),
              fill=(255, 255, 255), anchor="ma")
    # headline, 2 lines max
    yy = y + 166
    for line in wrap(draw, headline, font(SERIF, 23), w_ - 20)[:2]:
        draw.text((x + 10, yy), line, font=font(SERIF, 23), fill=NAVY)
        yy += 25
    # deck, 2 lines max
    yy = y + 218
    for line in wrap(draw, deck, font(SANS, 12), w_ - 20)[:2]:
        draw.text((x + 10, yy), line, font=font(SANS, 12), fill=INK)
        yy += 15
    draw.text((x + 10, y + 248), source, font=font(SANS, 10), fill=GREY)


def draw_grid_card(draw, x, y, w_, h_, story):
    n, region, headline, deck, status, source, kind, stat, stat_bg = story
    color = REGION_COLORS[region]
    draw.rectangle([x, y, x + w_, y + h_], fill=PANEL, outline=RULE, width=1)
    draw.rectangle([x, y, x + w_, y + 3], fill=color)
    # header: number + region (abbreviated so the pill never overlaps it),
    # pill at right
    draw.text((x + 8, y + 7), f"{n}", font=font(SANS_B, 12), fill=color)
    hdr_region = "E. ASIA & PAC." if region == "E. ASIA & PACIFIC" else region
    draw.text((x + 26, y + 8), hdr_region, font=font(SANS_B, 10), fill=GREY)
    pill(draw, (x + w_ - 8 - (draw.textlength(status, font=font(SANS_B, 10)) + 10),
                y + 6), status, font(SANS_B, 10), STATUS_FILL[status])
    # big flat mini-scene with stat chip bottom-right
    sx0, sy0, sx1, sy1 = x + 8, y + 24, x + w_ - 8, y + 60
    draw.rectangle([sx0, sy0, sx1, sy1], fill=tint(color))
    draw_grid_icon(draw, (sx0, sy0, sx1, sy1), kind, color)
    chip = stat
    cw = draw.textlength(chip, font=font(SANS_B, 11)) + 10
    draw.rectangle([sx1 - cw, sy1 - 18, sx1, sy1], fill=stat_bg)
    draw.text((sx1 - cw + 5, sy1 - 16), chip, font=font(SANS_B, 11),
              fill=(255, 255, 255))
    # headline, 2 lines max, 14 px serif
    yy = y + 64
    for line in wrap(draw, headline, font(SERIF, 14), w_ - 16)[:2]:
        draw.text((x + 8, yy), line, font=font(SERIF, 14), fill=NAVY)
        yy += 15
    # deck, 2 lines max, 10 px
    yy = y + 96
    for line in wrap(draw, deck, font(SANS, 10), w_ - 16)[:2]:
        draw.text((x + 8, yy), line, font=font(SANS, 10), fill=INK)
        yy += 11
    draw.text((x + w_ - 8, y + 118), source, font=font(SANS, 10),
              fill=GREY, anchor="ra")


# ---------------------------------------------------------------- map
# Continents in a 330x120 schematic space (simple tan blobs, like regian).
CONTINENTS = [
    [(8, 18), (30, 8), (55, 10), (70, 18), (62, 30), (45, 38), (30, 42), (12, 32)],  # N America
    [(55, 55), (72, 52), (78, 68), (68, 92), (58, 78)],                              # S America
    [(150, 12), (170, 8), (185, 14), (180, 26), (160, 30), (148, 22)],               # Europe
    [(138, 10), (143, 8), (145, 14), (140, 18)],                                     # UK
    [(150, 45), (175, 42), (190, 50), (185, 75), (165, 88), (152, 68)],              # Africa
    [(180, 82), (184, 80), (186, 90), (181, 92)],                                    # Madagascar
    [(190, 10), (260, 6), (310, 14), (315, 30), (300, 38), (275, 44), (255, 52),
     (240, 44), (215, 38), (195, 28)],                                               # Asia
    [(312, 22), (318, 20), (320, 28), (314, 32)],                                    # Japan
    [(272, 62), (290, 60), (296, 66), (278, 68)],                                    # Indonesia
    [(285, 85), (310, 82), (315, 95), (295, 100)],                                   # Australia
    [(308, 96), (313, 94), (315, 102), (309, 104)],                                  # New Zealand
]
PIN_REGION = {1: "MIDDLE EAST", 2: "MIDDLE EAST", 3: "N. AMERICA",
              4: "S. AMERICA", 5: "N. AMERICA", 6: "EUROPE", 7: "E. ASIA & PACIFIC",
              8: "AFRICA", 9: "EUROPE", 10: "MIDDLE EAST", 11: "S. ASIA",
              12: "E. ASIA & PACIFIC", 13: "EUROPE"}
# Pins in map-panel coordinates (ocean is 310x106). (n, true lon, true lat,
# pin x, pin y, leader?) Pin centres are all >=26 px apart (audit in the
# self-score); pins moved off their true spot get a short leader line to
# a small dot at the true location. Pin diameter 20 px.
PINS = [
    (1, 57, 26, 224, 770, False),
    (2, 47, 25, 196, 806, True),
    (3, -74, 41, 111, 761, False),
    (4, -75, 10, 92, 812, True),
    (5, -74, 41, 138, 738, True),
    (6, 35, 48, 238, 744, True),
    (7, 96, 21, 268, 808, True),
    (8, -17, 15, 148, 810, True),
    (9, 4, 51, 172, 786, True),
    (10, 34, 31, 196, 762, True),
    (11, 88, 28, 252, 782, True),
    (12, 100, 40, 272, 762, True),
    (13, -0.1, 51.5, 158, 758, True),
]


def draw_map(draw, x, y, w_, h_):
    draw.rectangle([x, y, x + w_, y + h_], fill=PANEL, outline=RULE, width=1)
    ox, oy = x + 6, y + 4
    ow, oh = w_ - 12, 106
    draw.rectangle([ox, oy, ox + ow, oy + oh], fill=OCEAN)
    for poly in CONTINENTS:
        pts = [(ox + px / 330 * ow, oy + py / 120 * oh) for px, py in poly]
        draw.polygon(pts, fill=LAND, outline=LAND_LINE)
    for n, lon, lat, px, py, leader in PINS:
        tx = ox + (lon + 180) / 360 * ow
        ty = oy + (90 - lat) / 180 * oh
        c = REGION_COLORS[PIN_REGION[n]]
        if leader:
            draw.line([tx, ty, px, py], fill=GREY, width=1)
            draw.ellipse([tx - 3, ty - 3, tx + 3, ty + 3], fill=c,
                         outline=(255, 255, 255), width=1)
        draw.ellipse([px - 10, py - 10, px + 10, py + 10], fill=c,
                     outline=(255, 255, 255), width=2)
        draw.text((px, py - 1), str(n), font=font(SANS_B, 12),
                  fill=(255, 255, 255), anchor="mm")
    draw.text((x + 8, y + 116), "Pins 1-13 = stories 1-13, color-coded by region.",
              font=font(SANS, 10), fill=GREY)
    draw.text((x + 8, y + 130),
              "Europe 6 · Middle East 7 · N. America 5 · E. Asia & Pac. 5",
              font=font(SANS_B, 10), fill=NAVY)
    draw.text((x + 8, y + 142),
              "S. America 4 · Africa 4 · S. Asia 2 · Global 2",
              font=font(SANS_B, 10), fill=NAVY)


# ---------------------------------------------------------------- page

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([4, 4, W - 5, H - 5], outline=NAVY, width=2)
    d.rectangle([8, 8, W - 9, H - 9], outline=GOLD, width=1)

    # masthead
    d.text((14, 8), "THE WORLD IN ONE DAY", font=font(SANS_B, 13), fill=RED)
    d.text((W - 14, 9), "35 DATED STORIES  •  8 REGIONS  •  14 FIELDS  •  ALL FROM TUE 24 NOV 2026 (UTC)",
           font=font(SANS_B, 11), fill=NAVY, anchor="ra")
    d.line([14, 28, W - 14, 28], fill=NAVY, width=2)

    # giant serif date
    d.text((W // 2, 32), "Tuesday 24 November 2026", font=font(SERIF, 60), fill=NAVY, anchor="ma")
    d.line([14, 92, W - 14, 92], fill=RULE, width=1)

    # subheadline: the 3 biggest stories, with specific numbers
    d.text((W // 2, 96), "HORMUZ: 3 TANKERS HIT  ◆  RIYADH TOWER: 11 HURT  ◆  NVIDIA +30%, NASDAQ +6.51%",
           font=font(SANS_B, 16), fill=RED, anchor="ma")

    # region strip: flat coloured pills with counts
    x = 14
    for name, cnt in REGIONS_STRIP:
        label = f"{name} {cnt}"
        w_ = d.textlength(label, font=font(SANS_B, 10)) + 14
        d.rounded_rectangle([x, 116, x + w_, 138], radius=3, fill=REGION_COLORS[name])
        d.text((x + 7, 121), label, font=font(SANS_B, 10), fill=(255, 255, 255))
        x += w_ + 5

    # timeline: one thin navy strip, honest times only (no PRESS TIME)
    d.rectangle([14, 142, W - 14, 168], fill=NAVY)
    d.text((20, 148), "TUESDAY IN UTC", font=font(SANS_B, 11), fill=(255, 210, 100))
    tx = 150
    for i, (t, ev) in enumerate(TIMELINE):
        d.text((tx, 149), t, font=font(SANS_B, 10), fill=(255, 255, 255))
        tx += d.textlength(t, font=font(SANS_B, 10)) + 5
        d.text((tx, 149), ev, font=font(SANS, 10), fill=(255, 255, 255))
        tx += d.textlength(ev, font=font(SANS, 10)) + 12
        if i < len(TIMELINE) - 1:
            d.text((tx, 149), "•", font=font(SANS_B, 10), fill=(255, 210, 100))
            tx += 12

    # heroes 170-434 (3 cols, 322 wide, 264 tall)
    hw = 322
    for i, story in enumerate(HEROES):
        draw_hero(d, 14 + i * (hw + 8), 170, hw, 264, story)

    # grid 4-13: 440-700, 5 cols x 2 rows, cards 192x128
    gw, gh = 192, 128
    for i, story in enumerate(GRID):
        col, row = i % 5, i // 5
        draw_grid_card(d, 14 + col * (gw + 8), 440 + row * (gh + 4), gw, gh, story)

    # section headers
    d.rectangle([14, 708, 22, 716], fill=RED)
    d.text((26, 705), "WHERE IT HAPPENED", font=font(SANS_B, 12), fill=NAVY)
    d.rectangle([346, 708, 354, 716], fill=RED)
    d.text((358, 705), "ALSO ON TUESDAY 24 NOVEMBER — 22 MORE DATED BRIEFS",
           font=font(SANS_B, 12), fill=NAVY)

    # map 728-880 (322 wide) + briefs (two columns of 11)
    draw_map(d, 14, 728, 322, 152)
    d.line([342, 730, 342, 876], fill=RULE, width=1)
    for col in range(2):
        bx = 350 + col * 336
        for j in range(11):
            n, region, text, src = BRIEFS[col * 11 + j]
            yy = 730 + j * 13
            c = REGION_COLORS[region]
            d.text((bx, yy), f"{n}.", font=font(SANS_B, 10), fill=c)
            src_w = d.textlength(src, font=font(SANS, 10))
            max_tw = 322 - 26 - src_w - 6
            while d.textlength(text, font=font(SANS, 10)) > max_tw and len(text) > 10:
                text = text[:-2]
            if text != BRIEFS[col * 11 + j][2]:
                text = text.rstrip() + "…"
            d.text((bx + 26, yy), text, font=font(SANS, 10), fill=INK)
            d.text((bx + 322, yy), src, font=font(SANS, 10), fill=GREY, anchor="ra")

    # date check 886-958 (3 text lines: 2 excluded + 1 not-yet)
    d.rectangle([14, 886, W - 14, 958], outline=RED, width=2)
    d.rectangle([14, 886, W - 14, 908], fill=RED)
    d.text((20, 890), "DATE CHECK — EXCLUDED", font=font(SANS_B, 12),
           fill=(255, 255, 255))
    d.text((20, 913),
           "EXCLUDED: COP31 ended 22 Nov (only reactions 24 Nov)  •  ICJ Rohingya ruling was 19 Nov  •  Nvidia CEO restored 23 Nov (market jump 24 Nov)  •  *Hormuz: 20:25 UTC 23 Nov",
           font=font(SANS, 11), fill=INK)
    d.text((20, 928),
           "EXCLUDED: Shenzhou-24 launch 25 Nov 00:18 UTC (crew named 24 Nov)  •  NOT YET: Cartagena rescue finished early 25 Nov",
           font=font(SANS, 11), fill=INK)
    d.text((20, 943),
           "NOT YET: Houthi claim on Riyadh came 25 Nov  •  Australia-Solomon deal signed 25 Nov",
           font=font(SANS, 11), fill=INK)

    # footer 962-1012, all 10 px
    d.text((14, 962),
           "HOW SURE:  CONFIRMED = 2+ outlets  •  OFFICIAL = on the record  •  REPORTED = single wire / local  •  CLAIM = one side's account, unverified",
           font=font(SANS_B, 10), fill=NAVY)
    d.text((14, 976),
           "All 35 stories are dated Tuesday 24 November 2026 (UTC). Scenes and map are drawn in code, not photographs.",
           font=font(SANS, 10), fill=INK)
    d.text((14, 990),
           "Sources: Reuters, AP, BBC, Al Jazeera, NPR, CNN, DW, France 24, SCMP, NHK, ABC Australia, Politico, Foreign Policy, The Guardian,",
           font=font(SANS, 10), fill=GREY)
    d.text((14, 1002),
           "UN News, Oxfam/CEOBS, MI5/NPSA, UKMTO/JMIC, Xinhua/CMSA, CAS, USGS/NEMRC, Jeune Afrique, Yonhap.  •  Tuesday 24 November 2026  •  The World in One Day",
           font=font(SANS, 10), fill=GREY)
    return img


def main():
    img = build()
    here = os.path.dirname(os.path.abspath(__file__))
    local = os.path.join(here, "entry.png")
    img.save(local, format="PNG", optimize=True)
    try:
        os.makedirs("/output", exist_ok=True)
        img.save("/output/entry.png", format="PNG", optimize=True)
    except Exception:
        pass
    print(f"wrote {local}  {img.size[0]}x{img.size[1]}  {os.path.getsize(local)} bytes")


if __name__ == "__main__":
    main()
