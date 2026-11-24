#!/usr/bin/env python3
"""ALMANAC - one-page data almanac of Monday 23 November 2026 world news.
Renders entry.png (1024x1024) with PIL. Run: python3 render.py"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(HERE, "fonts")
W, H = 1024, 1024

BG = (15, 42, 48)          # deep slate-teal
PANEL = (22, 58, 66)
PANEL2 = (27, 70, 79)
INK = (242, 245, 243)      # light text
MUT = (178, 205, 199)      # muted text
ACC = (87, 208, 196)       # teal accent
AMB = (255, 180, 84)       # amber
RED = (255, 107, 94)
BLU = (106, 168, 255)
GRN = (140, 220, 150)
DARK = (10, 26, 31)

def F(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)

def sans(size):  return F("LiberationSans-Regular.ttf", size)
def bold(size):  return F("LiberationSans-Bold.ttf", size)
def serif(size): return F("LiberationSerif-Bold.ttf", size)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img, "RGBA")

def tw(txt, font):
    b = d.textbbox((0, 0), txt, font=font)
    return b[2] - b[0]

def fit_font(txt, maker, start, maxw):
    s = start
    while s > 10 and tw(txt, maker(s)) > maxw:
        s -= 2
    return maker(s)

def wrap(txt, font, maxw):
    out, cur = [], ""
    for w_ in txt.split():
        t = (cur + " " + w_).strip()
        if tw(t, font) <= maxw:
            cur = t
        else:
            if cur: out.append(cur)
            cur = w_
    if cur: out.append(cur)
    return out

def text(x, y, txt, font, fill=INK, anchor="la"):
    d.text((x, y), txt, font=font, fill=fill, anchor=anchor)

def chip(x, y, txt, fill, fg=DARK, font=None, pad=6):
    font = font or bold(14)
    w_ = tw(txt, font) + pad * 2
    d.rounded_rectangle([x, y, x + w_, y + 24], 5, fill=fill)
    text(x + pad, y + 3, txt, font, fg)
    return w_

# ---------------- content (own wording, facts from the day) ----------------
DATE_LINE = "MONDAY 23 NOVEMBER 2026"
COUNT_LINE = "38 STORIES  ·  7 REGIONS  ·  EVERY ONE FROM THIS MONDAY"

LEADS = [
    dict(label="NO DEAL", color=AMB,
         head="COP31 TALKS END WITH NO DEAL",
         summ="Longest climate summit ever ends in Türkiye with no deal.",
         tag="CONFIRMED · BBC, The Guardian"),
    dict(label="SEA DRONE STRIKE", color=RED,
         head="RUSSIAN CORVETTE SUNK AT BENGHAZI",
         summ="Suspected Ukrainian sea drone sinks it at a Libyan fuel stop.",
         tag="CONFIRMED · BBC, Al Jazeera"),
    dict(label="ALIVE AFTER 14 HOURS", color=GRN,
         head="BOY, 7, FREED FROM RUBBLE",
         summ="David, 7, freed after 14 hours under a struck Dymer block.",
         tag="CONFIRMED · BBC, Al Jazeera"),
    dict(label="258 SEATS", color=BLU,
         head="DEMOCRATS WIN 258 HOUSE SEATS",
         summ="A Carolina flip gives the biggest majority since 1992.",
         tag="OFFICIAL · BBC, Al Jazeera"),
]

# icon key, headline, summary, tag
TIER2 = [
    ("plane",  "BELGIUM'S AIRPORTS SHUT BY STRIKE", "Controllers walk out nationwide.", "REPORTED · Al Jazeera"),
    ("medic",  "WEST BANK MEDIC ATTACKS UP 350%", "Rights group counts surge.", "REPORTED · Al Jazeera, PHRI"),
    ("virus",  "EBOLA RESPONSE AT 'GRAVE RISK'", "Fighting threatens the response.", "CONFIRMED · BBC, WHO"),
    ("factory","FACTORY FIRE TOLL REACHES 24 DEAD", "Toll rises; 30 still missing.", "CONFIRMED · BBC Asia"),
    ("warn",   "ARMY TO BLOW UP 4T OF EXPLOSIVE", "Controlled blast planned in Iowa.", "REPORTED · BBC"),
    ("mic",    "RUSSIA PLOTTED KILLING OF RAPPER", "Warsaw accuses Moscow, twice.", "REPORTED · Al Jazeera"),
    ("arena",  "ARENA EVACUATED MID-CONCERT", "Co-op Live emptied mid-show.", "CONFIRMED · BBC"),
    ("chart",  "ASIAN MARKETS TUMBLE ON AI FEARS", "Tech sell-off deepens.", "REPORTED · Al Jazeera, BBC"),
    ("fist",   "'DESTROY CAPITALISM, NOT FRANCE'", "Marchers fill French streets.", "REPORTED · BBC"),
    ("shake",  "SYRIA–EU TALKS MOVE FORWARD", "Repatriation fears linger.", "REPORTED · Al Jazeera"),
]

NUMBERS = [
    ("258", "Dem House seats, most since 1992"),
    ("14 HRS", "boy, 7, trapped in Dymer rubble"),
    ("24", "dead in Indonesia factory fire"),
    ("350%", "rise in attacks on W. Bank medics"),
    ("4 TONS", "explosive US Army will blow up"),
    ("90M+", "Tamagotchi shipped as it turns 30"),
]

TIMELINE = [
    ("00:18", "Asian markets fall"), ("00:39", "WHO Ebola warning"),
    ("01:23", "Democrats hit 258"), ("01:53", "Poland plot claim"),
    ("02:35", "Factory toll 24"), ("02:59", "Corvette sunk"),
    ("03:15", "Belgium airports shut"), ("04:21", "Arena evacuated"),
    ("05:15", "COP31 collapses"), ("05:33", "Boy pulled alive"),
    ("05:38", "Medics figure out"), ("06:08", "Syria–EU talks"),
]

PINS = [  # number, lon, lat
    (1, 28.9, 41.0), (2, 20.1, 32.1), (3, 30.5, 50.4), (4, -77.0, 38.9),
    (5, 4.35, 50.85), (6, 35.2, 31.9), (7, 23.0, -2.5), (8, 107.0, -6.2),
    (9, -93.5, 42.0), (10, 21.0, 52.2), (11, -2.24, 53.5), (12, 114.2, 22.3),
]

# briefs: (region, [(bold lead, rest), ...]) — shortened, fact kept
BRIEFS = [
    ("EUROPE", [("NHS", " starts AI cancer trial"),
                ("Poundland", " days from collapse"),
                ("Protests", " sweep EU cities"),
                ("Man Utd", " lose 4–0 to Liverpool")]),
    ("N. AMERICA", [("Bayer", " Roundup deal OK'd"),
                    ("Trump", " threatens AI-centre ban"),
                    ("Riemann", " AI proof claimed"),
                    ("Rikers", " closes by 2032"),
                    ("UFO", " footage #8 out")]),
    ("ASIA–PACIFIC", [("Tamagotchi", " 30 yrs, 90m shipped"),
                      ("Onosato", " back-to-back sumo"),
                      ("Snow", " Fukushima: 1,000+ stranded"),
                      ("NZ–India", " Test drawn")]),
    ("AFRICA & MIDEAST", [("Nigeria", " decriminalises suicide"),
                          ("Cameroon", " ex-rebels fear arrest")]),
    ("LATIN AMERICA", [("Costa Rica", " reporter murdered")]),
    ("UNITED KINGDOM", [("PIP", " overhaul urged"),
                        ("RAF", " next jet 'last crewed'"),
                        ("Energy bills", " to soar")]),
    ("SPAIN", [("Feijóo", " leads polls")]),
]

DATE_CHECK = ("DATE CHECK — LEFT OUT (OLDER): Myanmar verdict 19 Nov · Venezuela–US deal 19 Nov · "
              "Van Gogh $190.4m 19 Nov · Cyrus wedding 22 Nov · Finland attack 22 Nov · NOT YET: Spain votes 29 Nov.")

# ---------------- drawing helpers ----------------
def panel(x, y, w_, h_, fill=PANEL):
    d.rounded_rectangle([x, y, x + w_, y + h_], 8, fill=fill)

def lead_art(i, x, y, w_, h_):
    """Literal mini-scene for lead i inside box (x,y,w_,h_)."""
    d.rounded_rectangle([x, y, x + w_, y + h_], 6, fill=(13, 34, 40))
    cx, cy = x + w_ // 2, y + h_ // 2
    if i == 0:  # COP31: cracked globe over a table
        r = 24
        d.ellipse([cx - r, cy - r - 4, cx + r, cy + r - 4], outline=ACC, width=3)
        d.line([cx - r, cy - 4, cx + r, cy - 4], fill=ACC, width=2)
        d.arc([cx - 12, cy - r - 4, cx + 12, cy + r - 4], 90, 270, fill=ACC, width=2)
        d.arc([cx - 12, cy - r - 4, cx + 12, cy + r - 4], 270, 90, fill=ACC, width=2)
        d.line([cx - 4, cy - r - 2, cx + 3, cy - 12, cx - 3, cy - 2, cx + 5, cy + 8, cx, cy + r - 6],
               fill=AMB, width=3)  # crack
        text(cx + r + 8, cy - 18, "1.5°C", bold(17), AMB)
        d.rectangle([x + 14, y + h_ - 12, x + w_ - 14, y + h_ - 7], fill=MUT)  # table
    elif i == 1:  # Benghazi: listing ship + drone boat at night
        d.polygon([(x + 40, cy + 6), (x + 150, cy + 6), (x + 138, cy + 22), (x + 52, cy + 22)],
                  fill=(140, 165, 180))  # hull, low on one side
        d.rectangle([x + 78, cy - 12, x + 112, cy + 6], fill=(170, 195, 210))
        d.line([x + 95, cy - 26, x + 95, cy - 12], fill=MUT, width=3)
        for wx in range(x + 16, x + w_ - 10, 26):  # waves
            d.arc([wx, y + h_ - 16, wx + 16, y + h_ - 4], 180, 360, fill=BLU, width=2)
        d.polygon([(x + w_ - 52, cy + 14), (x + w_ - 22, cy + 14), (x + w_ - 30, cy + 22),
                   (x + w_ - 46, cy + 22)], fill=RED)  # drone boat
        text(x + w_ - 48, cy - 2, "DRONE", bold(12), RED)
    elif i == 2:  # Dymer: rubble gap, rescuers passing a child
        for k, (rx, rh) in enumerate([(0, 16), (26, 26), (58, 12), (150, 22), (186, 14), (120, 10)]):
            d.polygon([(x + rx, y + h_), (x + rx + 14, y + h_ - rh), (x + rx + 30, y + h_)],
                      fill=(105, 115, 118))
        gy = y + h_ - 26
        for fx, col in [(84, AMB), (122, (255, 140, 60))]:  # two hi-vis rescuers
            d.ellipse([x + fx - 7, gy - 20, x + fx + 7, gy - 6], fill=(240, 210, 170))
            d.rectangle([x + fx - 8, gy - 6, x + fx + 8, gy + 16], fill=col)
        d.ellipse([x + 98, gy - 12, x + 110, gy], fill=(240, 210, 170))  # child head
        d.line([x + 94, gy + 2, x + 114, gy + 2], fill=GRN, width=5)         # child body passed across
    else:  # House: Capitol dome left, seat bars right
        dcx, dcy = x + 42, y + h_ - 16
        d.arc([dcx - 26, dcy - 26, dcx + 26, dcy + 14], 180, 360, fill=INK, width=3)
        d.rectangle([dcx - 32, dcy - 2, dcx + 32, dcy + 2], fill=INK)
        for vx in (-20, -7, 7, 20):
            d.line([dcx + vx, dcy + 2, dcx + vx, dcy + 12], fill=INK, width=2)
        d.line([dcx, dcy - 34, dcx, dcy - 26], fill=AMB, width=3)
        bx, bw = x + 96, w_ - 108
        d.rectangle([bx, y + 14, bx + bw * 258 // 431, y + 25], fill=BLU)
        text(bx + bw * 258 // 431 + 5, y + 13, "258", bold(14), BLU)
        d.rectangle([bx, y + 30, bx + bw * 173 // 431, y + 41], fill=RED)
        text(bx + bw * 173 // 431 + 5, y + 29, "173", bold(14), RED)

def icon(kind, x, y, s=34):
    """Simple pictogram in an accent-ringed box at (x,y), size s."""
    d.rounded_rectangle([x, y, x + s, y + s], 7, fill=PANEL2, outline=ACC, width=1)
    cx, cy = x + s // 2, y + s // 2
    if kind == "plane":
        d.polygon([(x + 7, cy + 5), (x + s - 7, cy - 6), (x + s - 11, cy + 7), (x + 11, cy + 9)], fill=INK)
        d.line([x + 6, y + s - 7, x + s - 6, y + 7], fill=RED, width=4)
    elif kind == "medic":
        d.rectangle([cx - 4, cy - 11, cx + 4, cy + 3], fill=RED)
        d.rectangle([cx - 9, cy - 8, cx + 9, cy - 2], fill=RED)
        d.polygon([(cx + 2, y + s - 8), (cx + 9, y + s - 15), (cx + 11, y + s - 7)], fill=GRN)
    elif kind == "virus":
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], outline=RED, width=3)
        for a in range(0, 360, 60):
            import math
            ex, ey = cx + int(12 * math.cos(math.radians(a))), cy + int(12 * math.sin(math.radians(a)))
            d.line([cx, cy, ex, ey], fill=RED, width=2)
    elif kind == "factory":
        d.polygon([(x + 6, y + s - 7), (x + 6, cy), (x + 15, cy + 4), (x + 15, y + s - 7)], fill=MUT)
        d.rectangle([x + 17, cy - 8, x + 21, y + s - 7], fill=MUT)
        d.polygon([(cx + 6, cy - 12), (cx + 12, cy - 2), (cx + 6, cy + 6), (cx + 1, cy - 2)], fill=(255, 140, 60))
    elif kind == "warn":
        d.polygon([(cx, y + 6), (x + s - 6, y + s - 7), (x + 6, y + s - 7)], outline=AMB, width=3)
        text(cx, cy - 3, "4t", bold(13), AMB, anchor="ma")
    elif kind == "mic":
        d.rounded_rectangle([cx - 4, y + 6, cx + 4, cy + 4], 4, fill=INK)
        d.arc([cx - 9, cy - 6, cx + 9, cy + 10], 0, 180, fill=INK, width=2)
        d.ellipse([cx + 7, cy + 5, cx + 15, cy + 13], outline=RED, width=2)
        d.line([cx + 11, cy + 2, cx + 11, cy + 16], fill=RED, width=2)
    elif kind == "arena":
        d.arc([x + 7, cy - 12, x + s - 7, cy + 14], 180, 360, fill=INK, width=3)
        d.line([x + 7, cy + 1, x + s - 7, cy + 1], fill=INK, width=3)
        d.polygon([(cx - 3, cy + 5), (cx + 4, cy + 9), (cx - 3, cy + 13)], fill=GRN)
        d.polygon([(cx + 6, cy + 5), (cx + 13, cy + 9), (cx + 6, cy + 13)], fill=GRN)
    elif kind == "chart":
        d.line([x + 7, y + 10, x + 14, cy + 2, x + 19, cy - 3, x + s - 7, y + s - 9], fill=RED, width=3)
        d.rectangle([cx + 3, y + s - 14, cx + 11, y + s - 6], outline=ACC, width=2)
    elif kind == "fist":
        d.rectangle([cx - 7, cy + 1, cx + 5, y + s - 6], fill=AMB)
        for fx in range(-7, 6, 4):
            d.rectangle([cx + fx, cy - 9, cx + fx + 3, cy + 2], fill=AMB)
        d.line([x + s - 9, y + 6, x + s - 9, y + s - 6], fill=BLU, width=2)
        d.polygon([(x + s - 9, y + 6), (x + s - 3, y + 9), (x + s - 9, y + 12)], fill=RED)
    else:  # shake: two hands + document
        d.rectangle([cx - 3, y + 6, cx + 9, cy + 6], fill=INK)
        d.polygon([(x + 6, cy + 2), (cx + 2, cy - 3), (cx + 6, cy + 4), (x + 10, cy + 8)], fill=MUT)
        d.polygon([(x + s - 6, cy + 2), (cx + 4, cy - 3), (cx + 2, cy + 6), (x + s - 10, cy + 8)], fill=MUT)

# simplified continent outlines in (lon, lat)
CONTINENTS = [
    [(-165, 68), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66), (-92, 57), (-80, 62),
     (-78, 58), (-80, 45), (-76, 35), (-75, 40), (-70, 42), (-66, 45), (-60, 46), (-65, 50),
     (-70, 44), (-75, 38), (-76, 34), (-80, 32), (-81, 26), (-84, 30), (-89, 30), (-94, 29),
     (-97, 26), (-97, 22), (-94, 18), (-90, 14), (-83, 9), (-79, 9), (-86, 13), (-92, 15),
     (-105, 20), (-110, 24), (-114, 29), (-120, 34), (-124, 40), (-124, 48), (-132, 56), (-152, 60)],
    [(-79, 9), (-72, 12), (-64, 10), (-55, 6), (-50, 0), (-44, -3), (-35, -8), (-39, -13),
     (-40, -21), (-48, -26), (-52, -32), (-58, -38), (-65, -41), (-65, -45), (-67, -50),
     (-68, -54), (-71, -54), (-73, -46), (-73, -37), (-71, -30), (-70, -18), (-75, -15),
     (-79, -8), (-80, -4), (-77, 4)],
    [(-10, 36), (-9, 43), (-1, 44), (0, 47), (-4, 49), (1, 51), (5, 53), (8, 55), (7, 58),
     (12, 56), (18, 55), (21, 55), (24, 58), (28, 59), (29, 63), (24, 67), (19, 70), (14, 67),
     (10, 62), (5, 61), (5, 58), (3, 53), (0, 46), (-2, 44), (-2, 37), (-6, 36)],
    [(30, 46), (32, 70), (45, 68), (60, 69), (75, 72), (95, 76), (110, 74), (130, 72),
     (150, 70), (170, 66), (178, 65), (170, 60), (158, 52), (142, 50), (140, 40), (135, 35),
     (129, 33), (122, 31), (120, 25), (110, 20), (108, 12), (105, 8), (103, 1), (100, 7),
     (98, 14), (92, 16), (89, 22), (86, 20), (80, 15), (77, 8), (72, 20), (66, 25), (61, 25),
     (57, 26), (52, 28), (50, 29), (48, 30), (55, 26), (59, 22), (55, 17), (52, 15), (45, 12),
     (43, 12), (40, 15), (38, 20), (35, 28), (34, 31), (36, 36), (30, 38), (28, 41)],
    [(-17, 15), (-10, 5), (-8, -2), (9, -1), (13, -12), (12, -18), (14, -22), (16, -29),
     (19, -34), (27, -34), (32, -28), (35, -24), (36, -20), (40, -15), (40, -10), (39, -5),
     (41, 1), (51, 11), (44, 11), (43, 15), (40, 20), (38, 24), (35, 28), (32, 31), (22, 33),
     (11, 34), (10, 37), (5, 37), (-2, 35), (-6, 35), (-10, 31), (-16, 24), (-17, 20)],
    [(113, -22), (114, -28), (115, -34), (118, -35), (124, -33), (129, -32), (132, -32),
     (135, -35), (138, -35), (140, -38), (145, -38), (150, -37), (153, -30), (153, -25),
     (151, -24), (146, -19), (142, -11), (142, -15), (136, -12), (135, -15), (132, -11),
     (126, -14), (122, -17), (117, -20)],
    [(-45, 60), (-40, 64), (-32, 68), (-22, 70), (-18, 66), (-22, 64), (-30, 60), (-42, 59)],
]

def draw_map(x, y, w_, h_):
    d.rounded_rectangle([x, y, x + w_, y + h_], 6, fill=(13, 34, 40))
    def px(lon, lat):
        return (x + (lon + 180) / 360 * w_, y + (90 - lat) / 180 * h_)
    for gx in range(-150, 181, 30):  # graticule
        a, b = px(gx, 85), px(gx, -58)
        d.line([a, b], fill=(30, 66, 72), width=1)
    for gy in range(-40, 81, 20):
        a, b = px(-180, gy), px(180, gy)
        d.line([a, b], fill=(30, 66, 72), width=1)
    land = (64, 122, 110)
    for poly in CONTINENTS:
        pts = [px(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=land)
    nudge = {11: (-12, -6), 5: (4, 11), 10: (15, -4), 3: (10, -9), 1: (12, 7), 6: (13, 9), 2: (-8, 11)}
    for num, lon, lat in PINS:
        cxp, cyp = px(lon, lat)
        dx, dy = nudge.get(num, (0, 0))
        cxp, cyp = cxp + dx, cyp + dy
        r = 13
        d.ellipse([cxp - r, cyp - r, cxp + r, cyp + r], fill=AMB, outline=DARK, width=2)
        text(cxp, cyp - 1, str(num), bold(15), DARK, anchor="ma")

# ---------------- page assembly ----------------
MX = 16            # side margin
CW = W - 2 * MX    # content width 992

# masthead: date largest on page
df = fit_font(DATE_LINE, serif, 92, CW)
text(W // 2, 0, DATE_LINE, df, INK, anchor="ma")
d.rectangle([0, 70, W, 92], fill=ACC)
text(W // 2, 74, COUNT_LINE, bold(16), DARK, anchor="ma")

# leads row
LY, LH = 98, 172
colw = (CW - 30) // 4
for i, L in enumerate(LEADS):
    x = MX + i * (colw + 10)
    panel(x, LY, colw, LH)
    lead_art(i, x + 6, LY + 6, colw - 12, 52)
    chip(x + 10, LY + 10, L["label"], L["color"], font=bold(13), pad=5)
    hy = LY + 62
    for ln in wrap(L["head"], bold(22), colw - 14):
        text(x + 7, hy, ln, bold(22), INK); hy += 25
    sy = LY + 114
    for ln in wrap(L["summ"], sans(16), colw - 14)[:2]:
        text(x + 7, sy, ln, sans(16), MUT); sy += 18
    text(x + 7, LY + 153, L["tag"], bold(13), L["color"])

# centrepiece: world map + pin numbers
text(MX, 278, "WHERE IT HAPPENED — 23 NOVEMBER IN 12 PLACES", bold(20), ACC)
draw_map(MX, 302, CW, 106)

# UTC timeline rail under the map
TY = 414
d.line([MX, TY + 4, MX + CW, TY + 4], fill=ACC, width=2)
cell = CW / 12
for i, (tm, lab) in enumerate(TIMELINE):
    x = MX + i * cell
    d.ellipse([x + 2, TY + 1, x + 8, TY + 7], fill=AMB)
    text(x + 2, TY + 10, tm, bold(15), INK)
    ly = TY + 28
    for ln in wrap(lab, sans(11), cell - 6)[:2]:
        text(x + 2, ly, ln, sans(11), MUT); ly += 12

# day-in-numbers rail
NY = 468
ncell = CW // 6
for i, (fig, cap) in enumerate(NUMBERS):
    x = MX + i * ncell
    if i: d.line([x - 4, NY + 2, x - 4, NY + 44], fill=PANEL2, width=2)
    text(x + 2, NY, fig, bold(27), AMB)
    cy = NY + 30
    for ln in wrap(cap, sans(13), ncell - 12)[:2]:
        text(x + 2, cy, ln, sans(13), MUT); cy += 14

# tier-2 grid
GY = 534
text(MX, GY, "HOW SURE — CONFIRMED = 2+ independent outlets · OFFICIAL = on the record · REPORTED = one outlet / one side",
     bold(15), ACC)
rows_y = GY + 24
col2 = (CW - 12) // 2
for idx, (ic, head, summ, tag) in enumerate(TIER2):
    cx_ = MX + (idx % 2) * (col2 + 12)
    ry = rows_y + (idx // 2) * 43
    icon(ic, cx_, ry + 3)
    hx = cx_ + 44
    hf = fit_font(head, bold, 24, col2 - 48)
    text(hx, ry, head, hf, INK)
    text(hx, ry + 26, summ + "  " + tag, sans(17), MUT)

# briefs: flowing rich text, bold lead words, region heads in accent
BY = 780
segs = []
for gi, (region, items) in enumerate(BRIEFS):
    segs.append((region + " — ", bold(22), ACC))
    for j, (lead, rest) in enumerate(items):
        segs.append((lead, bold(22), INK))
        tail = rest + (" · " if j < len(items) - 1 or gi < len(BRIEFS) - 1 else "")
        segs.append((tail, sans(22), MUT))
# lay out word by word
words = []
for txt_, fnt, col in segs:
    for w_ in txt_.split(" "):
        if w_: words.append((w_, fnt, col))
bx, by = MX, BY
SPACE = 6
for w_, fnt, col in words:
    ww = tw(w_, fnt)
    if bx + ww > MX + CW:
        bx = MX; by += 24
    text(bx, by, w_, fnt, col)
    bx += ww + SPACE

# footer: DATE CHECK strip
d.rectangle([0, 970, W, H], fill=AMB)
fy = 977
for ln in wrap(DATE_CHECK, bold(18), CW)[:2]:
    text(W // 2, fy, ln, bold(18), DARK, anchor="ma"); fy += 25

out = os.path.join(HERE, "entry.png")
img.save(out, optimize=True)
print("saved", out, os.path.getsize(out), "bytes")
