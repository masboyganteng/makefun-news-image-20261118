#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news front page (1024x1024 PNG).

One flat-design newspaper infographic: masthead + date, a hero panel for the
U.S.-Iran escalation with a hand-drawn sea scene, a 2x3 grid of secondary
stories with small flat icons, and an "Also today" strip. Every letter is
rendered by this script with PIL; no external image is used.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 26                      # outer margin
CW = W - 2 * M              # content width: 972

PAPER = (251, 247, 236)
INK = (26, 26, 26)
RED = (185, 28, 28)
NAVY = (30, 58, 95)
SEA = (22, 50, 74)
SKY = (220, 233, 242)
SAND = (222, 205, 170)
GREY = (96, 96, 96)
RULE = (180, 170, 150)
CELL = (255, 255, 255)
CELL_LINE = (216, 208, 190)
ICON_BG = (240, 234, 216)

FD = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 60)
F_DATE = font("DejaVuSans-Bold.ttf", 32)
F_KICKER = font("DejaVuSans-Bold.ttf", 19)
F_HERO = font("DejaVuSans-Bold.ttf", 42)
F_HERO_SUB = font("DejaVuSans.ttf", 22)
F_FACT = font("DejaVuSans-Bold.ttf", 19)
F_LABEL = font("DejaVuSans-Bold.ttf", 15)
F_HEAD = font("DejaVuSans-Bold.ttf", 21)
F_SUB = font("DejaVuSans.ttf", 15)
F_STRIP_LBL = font("DejaVuSans-Bold.ttf", 18)
F_STRIP = font("DejaVuSans.ttf", 15)
F_FOOT = font("DejaVuSans.ttf", 13)
F_SEA_LBL = font("DejaVuSans-Bold.ttf", 15)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_c(draw, cx, y, s, fnt, fill):
    draw.text((cx - draw.textlength(s, font=fnt) / 2, y), s, font=fnt, fill=fill)


def starburst(draw, cx, cy, r1, r2, n, fill):
    import math
    pts = []
    for i in range(2 * n):
        r = r1 if i % 2 == 0 else r2
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def draw_sea_scene(d, x0, y0, w, h):
    """Flat-design Gulf of Oman: sky, sea, strait shores, tanker, blast."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=SKY)
    sea_y = y0 + int(h * 0.48)
    d.rectangle([x0, sea_y, x0 + w, y0 + h], fill=SEA)
    # distant shores left and right of the strait
    d.polygon([(x0, sea_y), (x0 + 250, sea_y), (x0 + 190, sea_y - 26),
               (x0, sea_y - 18)], fill=SAND)
    d.polygon([(x0 + w, sea_y), (x0 + w - 260, sea_y), (x0 + w - 200, sea_y - 24),
               (x0 + w, sea_y - 16)], fill=SAND)
    # tanker hull
    hx0, hx1 = x0 + 300, x0 + 640
    hy0, hy1 = sea_y + 18, sea_y + 52
    d.polygon([(hx0, hy0), (hx1 - 60, hy0), (hx1, hy0 + 14), (hx1 - 30, hy1),
               (hx0, hy1)], fill=(31, 41, 55))
    d.line([(hx0, hy0 + 4), (hx1 - 58, hy0 + 4)], fill=(185, 28, 28), width=3)
    for px in range(hx0 + 24, hx1 - 70, 34):
        d.ellipse([px, hy0 + 14, px + 5, hy0 + 19], fill=(220, 233, 242))
    d.rectangle([hx0 + 8, hy0 - 16, hx0 + 120, hy0], fill=(185, 28, 28))
    d.rectangle([hx0 + 128, hy0 - 16, hx0 + 220, hy0], fill=(217, 119, 6))
    d.rectangle([hx0 + 228, hy0 - 16, hx0 + 300, hy0], fill=(37, 99, 235))
    d.rectangle([hx1 - 58, hy0 - 34, hx1 - 22, hy0], fill=(245, 245, 244))
    d.rectangle([hx1 - 52, hy0 - 44, hx1 - 28, hy0 - 34], fill=(185, 28, 28))
    # wake lines
    for i, yy in enumerate((hy1 + 6, hy1 + 12)):
        d.line([(hx0 + 30 + i * 40, yy), (hx1 - 40, yy)], fill=(120, 160, 190), width=2)
    # smoke plumes (kept inside the scene: top of highest circle >= y0 + 4)
    for (sx, sy, sr) in ((hx0 + 140, sea_y - 12, 16), (hx0 + 192, sea_y - 6, 18),
                         (hx0 + 166, sea_y - 2, 14)):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(107, 114, 128))
    # explosion starburst crowning the smoke column
    starburst(d, hx0 + 168, y0 + 32, 24, 11, 10, (249, 115, 22))
    starburst(d, hx0 + 168, y0 + 32, 14, 6, 10, (251, 191, 36))
    # missile arcs from the right
    d.arc([x0 + w - 260, y0 + 4, x0 + w - 60, y0 + 108], start=200, end=330,
          fill=(255, 255, 255), width=3)
    d.arc([x0 + w - 300, y0 + 30, x0 + w - 120, y0 + 120], start=200, end=330,
          fill=(255, 255, 255), width=3)
    d.ellipse([x0 + w - 96, y0 + 78, x0 + w - 88, y0 + 86], fill=(255, 255, 255))
    d.text((x0 + w - 218, y0 + h - 24), "GULF OF OMAN", font=F_SEA_LBL,
           fill=(220, 233, 242))


def icon_bridge(d, x, y, s):
    d.line([(x + 4, y + s - 12), (x + s - 4, y + s - 12)], fill=NAVY, width=4)
    d.arc([x + 6, y + 8, x + s - 6, y + s - 2], start=180, end=360, fill=NAVY, width=4)
    for px in (x + 12, x + s // 2, x + s - 12):
        d.line([(px, y + 14), (px, y + s - 12)], fill=NAVY, width=3)


def icon_tent(d, x, y, s):
    d.polygon([(x + s // 2, y + 8), (x + 6, y + s - 10), (x + s - 6, y + s - 10)],
              fill=(217, 119, 6))
    d.polygon([(x + s // 2, y + 30), (x + s // 2 - 10, y + s - 10),
               (x + s // 2 + 10, y + s - 10)], fill=(120, 53, 15))
    # small snowflake in the top-right corner of the icon box
    cx, cy, r = x + s - 12, y + 12, 7
    d.line([(cx - r, cy), (cx + r, cy)], fill=NAVY, width=2)
    d.line([(cx, cy - r), (cx, cy + r)], fill=NAVY, width=2)
    d.line([(cx - 5, cy - 5), (cx + 5, cy + 5)], fill=NAVY, width=2)
    d.line([(cx - 5, cy + 5), (cx + 5, cy - 5)], fill=NAVY, width=2)


def icon_globe(d, x, y, s):
    cx, cy, r = x + s // 2, y + s // 2, s // 2 - 4
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=4)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=NAVY, width=2)
    d.line([(cx - r, cy), (cx + r, cy)], fill=NAVY, width=2)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], start=200, end=340,
          fill=NAVY, width=2)


def icon_ballot(d, x, y, s):
    d.rectangle([x + 8, y + 18, x + s - 8, y + s - 8], outline=NAVY, width=4)
    d.line([(x + 14, y + 12), (x + s - 14, y + 12)], fill=NAVY, width=4)
    d.line([(x + 14, y + 26), (x + 24, y + 38), (x + s - 12, y + 16)],
           fill=RED, width=4)


def icon_clapper(d, x, y, s):
    d.rectangle([x + 6, y + 4, x + s - 6, y + 24], outline=INK, width=3)
    d.polygon([(x + 6, y + 4), (x + s - 6, y + 4), (x + s - 6, y + 14),
               (x + 6, y + 14)], fill=INK)
    for i in range(3):
        xx = x + 12 + i * 14
        d.line([(xx, y + 5), (xx + 8, y + 13)], fill=(255, 255, 255), width=3)
    d.rectangle([x + 6, y + 24, x + s - 6, y + s - 8], outline=INK, width=3)
    d.text((x + 13, y + 28), "007", font=font("DejaVuSans-Bold.ttf", 18), fill=RED)


def icon_plane(d, x, y, s):
    d.polygon([(x + 6, y + s // 2 + 2), (x + s - 14, y + s // 2 - 8),
               (x + s - 4, y + s // 2 - 4), (x + s - 14, y + s // 2 + 2),
               (x + s - 6, y + s // 2 + 12), (x + s - 16, y + s // 2 + 8),
               (x + 16, y + s // 2 + 10)], fill=NAVY)
    d.polygon([(x + s // 2 - 2, y + s // 2 - 2), (x + s // 2 + 10, y + 8),
               (x + s // 2 + 16, y + 8), (x + s // 2 + 6, y + s // 2 + 2)],
              fill=NAVY)


ICONS = {"bridge": icon_bridge, "tent": icon_tent, "globe": icon_globe,
         "ballot": icon_ballot, "clapper": icon_clapper, "plane": icon_plane}

CELLS = [
    ("UKRAINE", NAVY, "bridge", "Kerch Bridge hit a second night",
     "Strikes on the Russia–Crimea link as Kyiv talks peace with U.S. envoys"),
    ("GAZA", RED, "tent", "Cold threatens Gaza's displaced",
     "UN warns of more deaths; 1.7m still homeless, 1.4m face acute hunger"),
    ("CLIMATE", (15, 118, 110), "globe", "COP31 talks hit crunch time",
     "144 items still disputed in Antalya draft; summit ends Friday"),
    ("U.S. VOTE", NAVY, "ballot", "Peltola wins Alaska Senate",
     "Democrats reach 56 seats — first Alaska win since 2008"),
    ("FILM", RED, "clapper", "Pattinson is the new Bond",
     "Robert Pattinson named the next James Bond"),
    ("RUSSIA", (90, 90, 90), "plane", "Military plane crash kills 19",
     "An-12 comes down in Kemerovo region"),
]

STRIP = [
    "Romania hit by 5.3 quake",
    "U.S. measles cases worst in 40 years",
    "Waymo pulls driverless taxis off U.S. freeways",
    "Trump in Manila for Quad talks",
    "Estonia to shut Russia border in Dec",
    "Prague crowds demand free media",
    "Spain general strike hits ports",
    "Herzog taps Eisenkot to form Israeli government",
    "Nvidia posts strong quarter",
    "Apple services down",
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.line([(M, 30), (W - M, 30)], fill=INK, width=3)
    text_c(d, W // 2, 42, "THE WORLD IN ONE DAY", F_TITLE, INK)
    text_c(d, W // 2, 112, "WEDNESDAY, 18 NOVEMBER 2026", F_DATE, RED)
    d.line([(M, 152), (W - M, 152)], fill=INK, width=2)
    d.line([(M, 157), (W - M, 157)], fill=INK, width=1)

    # ---- hero panel ----
    hy0, hy1 = 172, 512
    d.rectangle([M, hy0, W - M, hy1], outline=INK, width=2)
    d.text((M + 14, hy0 + 10), "LEAD STORY  —  MIDDLE EAST", font=F_KICKER, fill=RED)
    draw_sea_scene(d, M + 2, hy0 + 40, CW - 4, 136)
    ty = hy0 + 186
    d.text((M + 14, ty), "U.S. DESTROYS 5 IRANIAN TANKERS", font=F_HERO, fill=INK)
    sub = ("Tehran hits 10 ships near Hormuz and fires missiles at a U.S. base "
           "in Jordan, after the IRGC twice targeted an American warship.")
    sy = ty + 56
    for line in wrap(d, sub, F_HERO_SUB, CW - 28):
        d.text((M + 14, sy), line, font=F_HERO_SUB, fill=INK)
        sy += 28
    d.text((M + 14, hy1 - 34),
           "Five tankers destroyed: Kaviz  •  Charminar  •  Horizon 1  •  Riesco  •  Derya",
           font=F_FACT, fill=RED)

    # ---- secondary grid 2 x 3 ----
    gx, gy = M, 528
    cw, ch, gap = 313, 162, 16
    for i, (label, color, icon, head, sub) in enumerate(CELLS):
        cx = gx + (i % 3) * (cw + gap)
        cy = gy + (i // 3) * (ch + gap)
        d.rectangle([cx, cy, cx + cw, cy + ch], fill=CELL, outline=CELL_LINE, width=1)
        d.rectangle([cx, cy, cx + cw, cy + 26], fill=color)
        d.text((cx + 10, cy + 5), label, font=F_LABEL, fill=(255, 255, 255))
        d.rectangle([cx + 10, cy + 36, cx + 68, cy + 94], fill=ICON_BG,
                    outline=CELL_LINE, width=1)
        ICONS[icon](d, cx + 12, cy + 38, 54)
        hx, hw = cx + 78, cw - 88
        hy = cy + 38
        for line in wrap(d, head, F_HEAD, hw)[:2]:
            d.text((hx, hy), line, font=F_HEAD, fill=INK)
            hy += 25
        sy2 = cy + 102
        for line in wrap(d, sub, F_SUB, cw - 20)[:2]:
            d.text((cx + 10, sy2), line, font=F_SUB, fill=(64, 64, 64))
            sy2 += 19

    # ---- also-today strip ----
    sy0 = 884
    d.line([(M, sy0), (W - M, sy0)], fill=INK, width=2)
    d.text((M, sy0 + 10), "ALSO TODAY", font=F_STRIP_LBL, fill=RED)
    col_w = (CW - 40) // 2
    for i, item in enumerate(STRIP):
        col, row = i % 2, i // 2
        ix = M + col * (col_w + 40)
        iy = sy0 + 28 + row * 16
        d.text((ix, iy), "•  " + item, font=F_STRIP, fill=INK)
    d.line([(M, 998), (W - M, 998)], fill=RULE, width=1)
    text_c(d, W // 2, 1005, "Compiled from wire reports  •  Wednesday 18 November 2026",
           F_FOOT, GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
