#!/usr/bin/env python3
"""Render the make.fun news-image-20261119 entry 2/3 for agent 4.

Magazine-spread front page: navy masthead, 3 hero scene panels, 10 scene
cards, small flat world map, 22 one-line briefs, DATE CHECK footer.
Drawn entirely with PIL primitives from the brief's text (no copied art).
Output: entry.png, 1024x1024, <= 1 MiB.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (245, 238, 218)
PAPER = (250, 244, 228)
INK = (26, 26, 26)
BRICK = (163, 51, 39)
NAVY = (31, 42, 68)
NAVY_LT = (47, 63, 99)
GOLD = (176, 141, 62)
GOLD_LT = (214, 178, 105)
GREY = (90, 86, 76)
LINE = (60, 52, 40)
LAND = (232, 220, 192)
SEA = (172, 207, 231)
SKY = (213, 226, 235)

FD = "/usr/share/fonts/truetype/dejavu"

# handle to the page image, so scenes can paste a rotated stamp overlay
_IMG = [None]


def F(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: F("DejaVuSerif.ttf", s)
SERIF_I = lambda s: F("DejaVuSerif-Italic.ttf", s)
SERIF_BI = lambda s: F("DejaVuSerif-BoldItalic.ttf", s)
SANS = lambda s: F("DejaVuSans.ttf", s)
SANS_B = lambda s: F("DejaVuSans-Bold.ttf", s)
SANS_O = lambda s: F("DejaVuSans-Oblique.ttf", s)


def wrap(draw, text, font, width):
    """Greedy word wrap; returns list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, font, fill, leading=None, align="left", width=None):
    """Draw lines; returns y just past the last line."""
    lh = leading or int(font.size * 1.18)
    for ln in lines:
        if align == "center" and width is not None:
            draw.text((x + (width - draw.textlength(ln, font=font)) / 2, y), ln,
                      font=font, fill=fill)
        else:
            draw.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def hline(draw, x0, x1, y, fill=INK, w=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w)


def card_frame(draw, x, y, w, h, fill=(255, 255, 255)):
    # White card face on the cream page: the dark text on pale cream was
    # what washed out at 300px; white lifts headline/deck contrast.
    draw.rectangle([x, y, x + w - 1, y + h - 1], fill=fill, outline=INK, width=1)


def badge_num(draw, x, y, n, d=18):
    draw.ellipse([x, y, x + d, y + d], fill=BRICK, outline=INK, width=1)
    s = str(n)
    f = SANS_B(11 if len(s) < 2 else 10)
    tw = draw.textlength(s, font=f)
    draw.text((x + (d - tw) / 2, y + (d - f.size) / 2 - 1), s, font=f, fill=(255, 255, 255))


def tag(draw, x, y, label="REPORTED"):
    f = SANS_B(8)
    tw = draw.textlength(label, font=f)
    draw.rectangle([x, y, x + tw + 8, y + 12], fill=NAVY)
    draw.text((x + 4, y + 1), label, font=f, fill=(255, 255, 255))
    return x + tw + 8


# ---------------------------------------------------------------- scenes
def draw_flag_us(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK, width=1)
    for i in range(7):
        if i % 2 == 0:
            draw.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7], fill=BRICK)
    draw.rectangle([x, y, x + w * 0.42, y + h * 4 / 7], fill=NAVY)


def draw_flag_cn(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=BRICK, outline=INK, width=1)
    cx, cy = x + w * 0.22, y + h * 0.28
    for dx, dy, r in [(0, 0, 5), (12, -4, 2), (14, 3, 2), (11, 9, 2), (4, 9, 2)]:
        draw.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r], fill=GOLD_LT)


def draw_flag_ru(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK, width=1)
    draw.rectangle([x, y, x + w, y + h / 3], fill=(255, 255, 255))
    draw.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(40, 80, 160))
    draw.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=BRICK)


def draw_face(draw, cx, cy, r, hair, skin=(232, 190, 150), style="cap"):
    # ears
    for sx in (-1, 1):
        draw.ellipse([cx + sx * r - 2, cy - 1, cx + sx * r + 2, cy + 5],
                     fill=skin, outline=INK, width=1)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=skin, outline=INK, width=1)
    # soft cheek shading under the cheekbones
    draw.arc([cx - r * 0.75, cy + r * 0.05, cx - r * 0.05, cy + r * 0.65],
             10, 170, fill=(205, 158, 118), width=1)
    draw.arc([cx + r * 0.05, cy + r * 0.05, cx + r * 0.75, cy + r * 0.65],
             10, 170, fill=(205, 158, 118), width=1)
    if style == "flat":
        # straight fringe: flatter hair cap
        draw.pieslice([cx - r, cy - r, cx + r, cy + r * 0.1], 180, 360, fill=hair)
    else:
        # hair cap
        draw.pieslice([cx - r, cy - r, cx + r, cy + r * 0.4], 180, 360, fill=hair)
    if style == "sweep":
        # blond side-swept fringe over the forehead
        draw.polygon([(cx - r, cy - r + 3), (cx + r * 0.5, cy - r + 1),
                      (cx + r * 0.9, cy - r * 0.3), (cx - r * 0.7, cy - r * 0.15)],
                     fill=hair)
        # hair texture
        for dx in (-6, -1, 4):
            draw.line([(cx + dx, cy - r + 4), (cx + dx + 3, cy - r + 8)],
                      fill=(190, 158, 58), width=1)
    elif style == "recede":
        # receding hair: skin shows through the front hairline, grey at the sides
        draw.pieslice([cx - r, cy - r, cx + r, cy + r * 0.4], 205, 335, fill=skin)
        # forehead wrinkles
        draw.line([(cx - 6, cy - 8), (cx + 6, cy - 8)], fill=(185, 145, 112), width=1)
        draw.line([(cx - 5, cy - 6), (cx + 5, cy - 6)], fill=(185, 145, 112), width=1)
    # eyebrows
    for ex in (-r * 0.38, r * 0.38):
        draw.line([(cx + ex - 4, cy - 4), (cx + ex + 4, cy - 5 if ex < 0 else cy - 4)],
                  fill=hair, width=2)
    # eyes: white + pupil + upper lash line
    for ex in (-r * 0.38, r * 0.38):
        draw.ellipse([cx + ex - 3, cy - 1, cx + ex + 3, cy + 3],
                     fill=(255, 255, 255), outline=INK, width=1)
        draw.ellipse([cx + ex - 1, cy, cx + ex + 1, cy + 2], fill=INK)
        draw.line([(cx + ex - 3, cy - 1), (cx + ex + 3, cy - 1)], fill=INK, width=1)
    # nose: bridge + nostril arc
    draw.line([(cx, cy + 3), (cx - 1, cy + 6)], fill=(170, 125, 95), width=1)
    draw.arc([cx - 2, cy + 5, cx + 2, cy + 8], 0, 180, fill=(170, 125, 95), width=1)
    # mouth: lips with a centre line (slightly downturned for the receding style)
    if style == "recede":
        draw.arc([cx - 4, cy + 7, cx + 4, cy + 12], 200, 340, fill=(120, 40, 35), width=1)
        draw.ellipse([cx - 4, cy + 8, cx + 4, cy + 11], fill=(165, 70, 60))
        draw.line([(cx - 3, cy + 9), (cx + 3, cy + 9)], fill=(120, 40, 35), width=1)
    else:
        draw.ellipse([cx - 4, cy + 8, cx + 4, cy + 11], fill=(165, 70, 60))
        draw.line([(cx - 4, cy + 9), (cx + 4, cy + 9)], fill=(120, 40, 35), width=1)


def draw_leader(draw, cx, base_y, suit, tie, hair, name, style="cap"):
    """Seated leader behind a table; base_y is the table top."""
    body_h = 34
    draw.rectangle([cx - 34, base_y - body_h, cx + 34, base_y], fill=suit, outline=INK, width=1)
    draw.polygon([(cx - 8, base_y - body_h), (cx, base_y - body_h + 12),
                  (cx + 8, base_y - body_h), (cx + 5, base_y), (cx - 5, base_y)],
                 fill=(255, 255, 255))
    draw.polygon([(cx - 4, base_y - body_h + 9), (cx + 4, base_y - body_h + 9),
                  (cx + 2, base_y - 6), (cx - 2, base_y - 6)], fill=tie)
    draw_face(draw, cx, base_y - body_h - 13, 13, hair, style=style)
    # nameplate
    f = SANS_B(10)
    tw = draw.textlength(name, font=f)
    draw.rectangle([cx - tw / 2 - 7, base_y + 4, cx + tw / 2 + 7, base_y + 19],
                   fill=(255, 255, 255), outline=INK, width=1)
    draw.text((cx - tw / 2, base_y + 6), name, font=f, fill=INK)


def hero_apec(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(38, 54, 88))
    # banner
    f = SANS_B(11)
    label = "APEC 2026 \u00b7 SHENZHEN"
    tw = draw.textlength(label, font=f)
    draw.rectangle([x, y, x + w, y + 18], fill=GOLD)
    draw.text((x + (w - tw) / 2, y + 3), label, font=f, fill=NAVY)
    # flags row, clear of the leaders' heads below
    draw_flag_us(draw, x + 16, y + 21, 44, 14)
    draw_flag_cn(draw, x + w // 2 - 22, y + 21, 44, 14)
    draw_flag_ru(draw, x + w - 60, y + 21, 44, 14)
    table_y = y + h - 21
    draw.rectangle([x + 6, table_y, x + w - 6, y + h], fill=(122, 84, 52), outline=INK, width=1)
    draw.rectangle([x + 6, table_y, x + w - 6, table_y + 5], fill=(240, 230, 210))
    step = w // 3
    draw_leader(draw, x + step // 2, table_y, (30, 30, 34), BRICK, (226, 196, 90), "TRUMP", "sweep")
    draw_leader(draw, x + step + step // 2, table_y, (30, 30, 34), BRICK, (20, 20, 20), "XI", "flat")
    draw_leader(draw, x + 2 * step + step // 2, table_y, (30, 30, 34), (40, 80, 160), (200, 200, 200), "PUTIN", "recede")


def draw_scales(draw, cx, cy, s=1.0):
    # scales of justice, gold
    draw.line([(cx, cy - 34 * s), (cx, cy + 26 * s)], fill=GOLD, width=3)
    draw.line([(cx - 30 * s, cy - 22 * s), (cx + 30 * s, cy - 22 * s)], fill=GOLD, width=3)
    draw.ellipse([cx - 4, cy - 38 * s, cx + 4, cy - 30 * s], fill=GOLD)
    for sx in (-30 * s, 30 * s):
        draw.line([(cx + sx, cy - 22 * s), (cx + sx - 10 * s, cy + 2 * s)], fill=GOLD, width=2)
        draw.line([(cx + sx, cy - 22 * s), (cx + sx + 10 * s, cy + 2 * s)], fill=GOLD, width=2)
        draw.pieslice([cx + sx - 12 * s, cy + 2 * s, cx + sx + 12 * s, cy + 16 * s], 0, 180, fill=GOLD)


def hero_icj(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 214, 196))
    # court building, with brick courses, window mullions and a door
    # (kept inside the 116px scene so its plinth never touches the kicker below)
    bx, by, bw, bh = x + 16, y + 56, 150, 60
    draw.rectangle([bx, by, bx + bw, by + bh], fill=(246, 238, 220), outline=INK, width=2)
    draw.polygon([(bx - 6, by), (bx + bw / 2, by - 22), (bx + bw + 6, by)], fill=BRICK, outline=INK)
    # single architrave line under the pediment (the old stepped courses
    # read as jagged stairsteps when cropped)
    draw.line([(bx + 2, by - 2), (bx + bw - 2, by - 2)],
              fill=(120, 35, 26), width=2)
    for yy in range(by + 6, by + bh - 4, 5):
        draw.line([(bx + 1, yy), (bx + bw - 1, yy)], fill=(214, 196, 168), width=1)
    for i in range(5):
        cx = bx + 14 + i * 30
        draw.rectangle([cx - 5, by + 10, cx + 5, by + bh - 8], fill=NAVY)
        draw.line([(cx - 5, by + 20), (cx + 5, by + 20)], fill=(255, 255, 255), width=1)
        draw.line([(cx - 5, by + 30), (cx + 5, by + 30)], fill=(255, 255, 255), width=1)
        draw.line([(cx - 1, by + 10), (cx - 1, by + bh - 8)], fill=(255, 255, 255), width=1)
    # central door between the middle columns
    draw.rectangle([bx + bw / 2 - 8, by + bh - 18, bx + bw / 2 + 8, by + bh - 8],
                   fill=(90, 60, 35), outline=INK, width=1)
    draw.ellipse([bx + bw / 2 + 3, by + bh - 13, bx + bw / 2 + 6, by + bh - 10],
                 fill=GOLD_LT)
    draw.rectangle([bx - 8, by + bh - 4, bx + bw + 8, by + bh], fill=NAVY)
    # flag of Myanmar (small) on the building
    draw.rectangle([bx + bw - 30, by + 12, bx + bw - 8, by + 26], fill=(252, 210, 60), outline=INK, width=1)
    draw.rectangle([bx + bw - 30, by + 12, bx + bw - 8, by + 17], fill=(60, 120, 70))
    draw.rectangle([bx + bw - 30, by + 21, bx + bw - 8, by + 26], fill=BRICK)
    # scales, right side
    draw_scales(draw, x + w - 62, y + 78, 1.0)
    # red vote badge
    draw.ellipse([x + w - 62, y + 8, x + w - 8, y + 46], fill=BRICK, outline=INK, width=2)
    f = SANS_B(16)
    t = "9\u20136"
    tw = draw.textlength(t, font=f)
    draw.text((x + w - 35 - tw / 2, y + 16), t, font=f, fill=(255, 255, 255))
    # sky sun
    draw.ellipse([x + 14, y + 10, x + 40, y + 36], fill=GOLD_LT, outline=INK, width=1)


def hero_cop31(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(24, 96, 92))
    # globe: blue sphere with shaded side, three green continents, grid
    gx, gy, gr = x + 62, y + 62, 44
    draw.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(64, 140, 190), outline=INK, width=2)
    # darker shading crescent on the right (day/night side)
    draw.pieslice([gx - gr, gy - gr, gx + gr, gy + gr], 300, 65, fill=(42, 112, 162))
    draw.pieslice([gx - gr, gy - gr, gx + gr, gy + gr], 295, 60, fill=(52, 122, 172))
    # continents (irregular blobs, kept inside the circle)
    draw.polygon([(gx - 30, gy - 26), (gx - 20, gy - 32), (gx - 10, gy - 26),
                  (gx - 14, gy - 14), (gx - 20, gy - 4), (gx - 28, gy - 10),
                  (gx - 34, gy - 18)], fill=(74, 164, 88), outline=(40, 110, 60))
    draw.polygon([(gx - 2, gy - 30), (gx + 10, gy - 30), (gx + 18, gy - 22),
                  (gx + 12, gy - 10), (gx + 2, gy - 12), (gx - 4, gy - 22)],
                 fill=(74, 164, 88), outline=(40, 110, 60))
    draw.polygon([(gx + 6, gy + 6), (gx + 20, gy + 4), (gx + 30, gy + 12),
                  (gx + 24, gy + 26), (gx + 10, gy + 28), (gx + 2, gy + 18)],
                 fill=(74, 164, 88), outline=(40, 110, 60))
    draw.ellipse([gx - 34, gy + 14, gx - 26, gy + 22], fill=(74, 164, 88),
                 outline=(40, 110, 60))
    draw.ellipse([gx + 22, gy - 34, gx + 30, gy - 28], fill=(74, 164, 88),
                 outline=(40, 110, 60))
    # latitude chords + longitude arcs (grid)
    for dy in (-22, 0, 22):
        hw = int((gr * gr - dy * dy) ** 0.5) - 1
        draw.line([(gx - hw, gy + dy), (gx + hw, gy + dy)],
                  fill=(205, 228, 242), width=1)
    draw.arc([gx - 22, gy - gr, gx + 22, gy + gr], 270, 90, fill=(205, 228, 242), width=1)
    draw.arc([gx - 22, gy - gr, gx + 22, gy + gr], 90, 270, fill=(205, 228, 242), width=1)
    draw.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=INK, width=2)
    # highlight arc top-left
    draw.arc([gx - gr + 4, gy - gr + 4, gx + gr - 4, gy + gr - 4], 180, 280,
             fill=(235, 245, 252), width=2)
    # thermometer
    tx = x + 148
    draw.rounded_rectangle([tx, y + 22, tx + 16, y + 96], radius=8, fill=(255, 255, 255), outline=INK, width=1)
    draw.ellipse([tx - 7, y + 88, tx + 23, y + 112], fill=BRICK, outline=INK, width=1)
    draw.rectangle([tx + 5, y + 52, tx + 11, y + 96], fill=BRICK)
    draw.ellipse([tx - 3, y + 92, tx + 19, y + 108], fill=BRICK)
    # document
    dx, dy, dw, dh = x + 178, y + 20, 128, 84
    draw.rectangle([dx, dy, dx + dw, dy + dh], fill=(255, 255, 255), outline=INK, width=2)
    f = SANS_B(12)
    draw.text((dx + 8, dy + 8), "DRAFT DEAL \u00b7 19 NOV", font=SANS_B(9), fill=GREY)
    draw.text((dx + 8, dy + 24), "FOSSIL FUELS", font=f, fill=INK)
    draw.line([(dx + 6, dy + 36), (dx + dw - 6, dy + 30)], fill=BRICK, width=3)
    f2 = SANS_B(8)
    t2 = "$120bn ADAPTATION AID"
    draw.text((dx + 8, dy + 46), t2, font=f2, fill=INK)
    draw.line([(dx + 6, dy + 52), (dx + 8 + draw.textlength(t2, font=f2), dy + 52)], fill=BRICK, width=2)
    # CUT stamp
    f3 = SANS_B(20)
    t = "CUT"
    tw = draw.textlength(t, font=f3)
    draw.rectangle([dx + dw - tw - 18, dy + dh - 26, dx + dw - 6, dy + dh - 4],
                   outline=BRICK, width=3)
    draw.text((dx + dw - tw - 12, dy + dh - 24), t, font=f3, fill=BRICK)


# ---------------------------------------------------------------- card scenes
def scene_bridge(draw, x, y, w, h):
    # Cable-stayed bridge, recognisable as a bridge: two towers, stay
    # cables fanning to the deck, a train on the left span, and a broken
    # middle span with a big explosion + smoke (the old thin arc read as
    # an "abstract arc").
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.ellipse([x + w - 30, y + 6, x + w - 8, y + 28], fill=GOLD_LT, outline=INK, width=1)
    # sea + waves
    draw.rectangle([x, y + h - 12, x + w, y + h], fill=(70, 120, 170))
    draw.line([(x + 8, y + h - 7), (x + 40, y + h - 7)], fill=(255, 255, 255), width=1)
    draw.line([(x + w - 52, y + h - 5), (x + w - 14, y + h - 5)], fill=(255, 255, 255), width=1)
    deck_y = y + h - 24
    # towers
    for tx in (x + 52, x + 140):
        draw.rectangle([tx - 2, y + 6, tx + 2, deck_y], fill=INK)
        draw.rectangle([tx - 5, y + 4, tx + 5, y + 8], fill=INK)
    # stay cables from each tower top to the deck
    for tx in (x + 52, x + 140):
        for dx in (-38, -24, -10, 10, 24, 38):
            draw.line([(tx, y + 8), (tx + dx, deck_y)], fill=(60, 60, 60), width=1)
    # deck: left span + right span, broken in the middle
    draw.rectangle([x + 4, deck_y, x + 86, deck_y + 5], fill=(40, 40, 44), outline=INK, width=1)
    draw.rectangle([x + 106, deck_y, x + w - 4, deck_y + 5], fill=(40, 40, 44), outline=INK, width=1)
    # broken stub tilting down into the gap
    draw.polygon([(x + 86, deck_y), (x + 98, deck_y + 2), (x + 94, deck_y + 10),
                  (x + 84, deck_y + 8)], fill=(40, 40, 44), outline=INK)
    # railing posts on both spans
    for px in (x + 16, x + 40, x + 64, x + 122, x + 152, x + 178):
        draw.line([(px, deck_y - 5), (px, deck_y)], fill=INK, width=1)
    draw.line([(x + 6, deck_y - 5), (x + 84, deck_y - 5)], fill=INK, width=1)
    draw.line([(x + 108, deck_y - 5), (x + w - 6, deck_y - 5)], fill=INK, width=1)
    # halted train on the left span
    for cx0 in (x + 14, x + 32, x + 50):
        draw.rectangle([cx0, deck_y - 12, cx0 + 16, deck_y - 5], fill=BRICK, outline=INK, width=1)
        draw.rectangle([cx0 + 3, deck_y - 10, cx0 + 7, deck_y - 7], fill=(255, 255, 255))
        draw.rectangle([cx0 + 10, deck_y - 10, cx0 + 14, deck_y - 7], fill=(255, 255, 255))
    # explosion in the gap + smoke plume
    ex, ey = x + 96, deck_y - 8
    for dx, dy in [(0, -14), (11, -8), (13, 4), (5, 13), (-7, 12), (-13, 3), (-11, -9)]:
        draw.line([(ex, ey), (ex + dx, ey + dy)], fill=(230, 120, 30), width=3)
    draw.ellipse([ex - 8, ey - 8, ex + 8, ey + 8], fill=(240, 160, 40), outline=BRICK, width=1)
    draw.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=(255, 220, 90))
    for sx, sy, sr in [(x + 84, y + 6, 7), (x + 96, y + 2, 8), (x + 108, y + 7, 6)]:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 120, 120),
                     outline=(80, 80, 80), width=1)


def scene_riyadh(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(48, 62, 104))
    for sx, sy in [(14, 10), (60, 22), (110, 8), (160, 18), (40, 34), (140, 32)]:
        draw.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    # skyline
    for bx, bw, bh in [(6, 26, 26), (38, 20, 36), (64, 30, 22), (100, 22, 34), (128, 26, 24), (158, 24, 30)]:
        draw.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(88, 102, 142), outline=INK, width=1)
    # intercept burst + missile trails
    mx, my = x + w // 2, y + 18
    for dx, dy in [(0, -10), (9, -5), (10, 5), (0, 10), (-10, 5), (-9, -5)]:
        draw.line([(mx, my), (mx + dx, my + dy)], fill=GOLD_LT, width=2)
    draw.ellipse([mx - 5, my - 5, mx + 5, my + 5], fill=GOLD_LT)
    draw.line([(x + 20, y + h - 8), (mx - 8, my + 6)], fill=(255, 255, 255), width=2)
    draw.line([(x + w - 16, y + h - 6), (mx + 8, my + 4)], fill=(255, 255, 255), width=2)


def scene_cyclone(draw, x, y, w, h):
    # clean white spiral on blue sea/sky, kept clear of the panel edges
    draw.rectangle([x, y, x + w, y + h], fill=(86, 148, 196))
    cx, cy = x + w // 2, y + h // 2 - 3
    for r in (18, 13, 8, 4):
        draw.arc([cx - r, cy - r, cx + r, cy + r], 30 + r * 6, 310 + r * 6,
                 fill=(255, 255, 255), width=3)
    draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 255, 255))
    # coastline along the bottom
    draw.rectangle([x, y + h - 6, x + w, y + h], fill=(96, 158, 110))


def scene_court(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 214, 196))
    # court building, narrower than before so the stamp fits clear of it
    bx, by, bw, bh = x + 12, y + 20, 100, 28
    draw.rectangle([bx, by, bx + bw, by + bh], fill=(246, 238, 220), outline=INK, width=1)
    draw.polygon([(bx - 4, by), (bx + bw / 2, by - 12), (bx + bw + 4, by)], fill=BRICK, outline=INK)
    for i in range(4):
        cx = bx + 11 + i * 26
        draw.rectangle([cx - 4, by + 6, cx + 4, by + bh - 4], fill=NAVY)
    # gavel lowered to the bottom-right, clear of the stamp zone above it
    draw.line([(x + 160, y + 32), (x + 146, y + 44)], fill=INK, width=8)
    draw.line([(x + 160, y + 32), (x + 146, y + 44)], fill=(120, 80, 40), width=5)
    draw.rectangle([x + 136, y + 24, x + 184, y + 36], fill=(140, 95, 50), outline=INK, width=2)
    draw.line([(x + 136, y + 30), (x + 184, y + 30)], fill=(90, 55, 25), width=2)
    draw.line([(x + 160, y + 24), (x + 160, y + 36)], fill=(90, 55, 25), width=1)
    draw.rectangle([x + 128, y + 43, x + 182, y + 47], fill=(140, 95, 50), outline=INK, width=1)
    # red OVERTURNED stamp, small, in the clear sky at top-right —
    # it used to sit on top of the building's roof and columns
    if _IMG[0] is not None:
        st = Image.new("RGBA", (72, 15), (0, 0, 0, 0))
        sd = ImageDraw.Draw(st)
        sd.rectangle([1, 1, 70, 13], outline=BRICK, width=2)
        sd.text((4, 2), "OVERTURNED", font=SANS_B(8), fill=BRICK)
        st = st.rotate(-10, expand=True, resample=Image.BICUBIC)
        _IMG[0].paste(st, (x + 116, y + 1), st)


def scene_arctic(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(190, 215, 230))
    draw.polygon([(x, y + h), (x + 40, y + 14), (x + 80, y + h)], fill=(255, 255, 255), outline=INK)
    draw.polygon([(x + 60, y + h), (x + 110, y + 6), (x + 160, y + h)], fill=(235, 242, 248), outline=INK)
    draw.polygon([(x + 130, y + h), (x + 168, y + 20), (x + w, y + h)], fill=(255, 255, 255), outline=INK)
    # Denmark flag
    draw.rectangle([x + 8, y + 6, x + 38, y + 22], fill=BRICK, outline=INK, width=1)
    draw.rectangle([x + 16, y + 6, x + 20, y + 22], fill=(255, 255, 255))
    draw.rectangle([x + 8, y + 12, x + 38, y + 16], fill=(255, 255, 255))
    # 109-0 badge
    f = SANS_B(10)
    t = "109\u20130"
    tw = draw.textlength(t, font=f)
    draw.rectangle([x + w - tw - 14, y + 6, x + w - 6, y + 22], fill=BRICK, outline=INK, width=1)
    draw.text((x + w - tw - 10, y + 8), t, font=f, fill=(255, 255, 255))


def scene_stocks(draw, x, y, w, h):
    # Pure line chart: the old exchange-building silhouette (triangle
    # roof + block) read as an "odd house shape" on the chart.
    draw.rectangle([x, y, x + w, y + h], fill=(30, 90, 60))
    # faint grid
    for gy in (y + 12, y + 24, y + 36):
        draw.line([(x + 6, gy), (x + w - 6, gy)], fill=(60, 125, 90), width=1)
    pts = [(x + 10, y + h - 10), (x + 42, y + h - 16), (x + 70, y + h - 12),
           (x + 100, y + h - 24), (x + 128, y + h - 20), (x + 156, y + h - 32),
           (x + 182, y + h - 40)]
    draw.line(pts, fill=GOLD_LT, width=3)
    draw.polygon([(pts[-1][0] - 9, pts[-1][1] + 1), (pts[-1][0] + 3, pts[-1][1] - 9),
                  (pts[-1][0] + 10, pts[-1][1] + 3)], fill=GOLD_LT)
    f = SANS_B(11)
    draw.text((x + 8, y + 5), "ANT", font=f, fill=(255, 255, 255))
    f2 = SANS_B(9)
    draw.text((x + w - 44, y + h - 14), "+17%", font=f2, fill=GOLD_LT)


def scene_gta(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(148, 88, 178))
    draw.ellipse([x + w - 52, y + 4, x + w - 12, y + 34], fill=(255, 190, 90), outline=INK, width=1)
    # sunset band behind the skyline
    draw.rectangle([x, y + h - 36, x + w, y + h - 18], fill=(214, 130, 80))
    # skyline
    for bx, bw, bh in [(4, 22, 26), (30, 18, 38), (52, 26, 22), (82, 20, 34), (106, 24, 28), (134, 22, 40), (160, 24, 24)]:
        draw.rectangle([x + bx, y + h - 18 - bh, x + bx + bw, y + h - 18], fill=(78, 44, 118), outline=INK, width=1)
    draw.rectangle([x, y + h - 18, x + w, y + h], fill=(40, 40, 44))
    # car
    draw.rounded_rectangle([x + 60, y + h - 16, x + 130, y + h - 4], radius=4, fill=BRICK, outline=INK, width=1)
    draw.ellipse([x + 70, y + h - 6, x + 80, y + h + 2], fill=INK)
    draw.ellipse([x + 110, y + h - 6, x + 120, y + h + 2], fill=INK)
    # VI sign
    f = SERIF_B(20)
    draw.text((x + 8, y + 2), "VI", font=f, fill=(255, 255, 255))


def scene_strike(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(240, 225, 190))
    # crowd heads
    cols = [(163, 51, 39), (31, 42, 68), (60, 120, 70), (176, 141, 62), (120, 70, 160)]
    for i in range(7):
        cx = x + 16 + i * 24
        draw.ellipse([cx - 8, y + h - 26, cx + 8, y + h - 10], fill=cols[i % 5], outline=INK, width=1)
        draw.rectangle([cx - 10, y + h - 12, cx + 10, y + h], fill=cols[i % 5])
    # banner
    draw.rectangle([x + 20, y + 8, x + w - 20, y + 26], fill=(255, 255, 255), outline=INK, width=1)
    f = SANS_B(9)
    t = "PARO NACIONAL"
    tw = draw.textlength(t, font=f)
    draw.text((x + (w - tw) / 2, y + 12), t, font=f, fill=BRICK)


def scene_runner(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(235, 225, 205))
    # track
    draw.rectangle([x, y + h - 20, x + w, y + h], fill=(180, 70, 50))
    draw.line([(x, y + h - 10), (x + w, y + h - 10)], fill=(255, 255, 255), width=1)
    # motion lines behind the runner
    draw.line([(x + 18, y + 14), (x + 40, y + 14)], fill=(150, 140, 120), width=2)
    draw.line([(x + 24, y + 22), (x + 44, y + 22)], fill=(150, 140, 120), width=2)
    # runner: filled silhouette mid-stride (dark kit, skin head)
    rx, ry = x + 78, y + 13
    BODY = (38, 30, 26)
    SKIN = (198, 148, 108)
    # back leg (extended behind)
    draw.line([(rx - 6, ry + 22), (rx - 18, ry + 26)], fill=BODY, width=6)
    draw.line([(rx - 18, ry + 26), (rx - 26, ry + 36)], fill=BODY, width=6)
    # front leg (bent, driving forward)
    draw.line([(rx - 6, ry + 22), (rx + 6, ry + 28)], fill=BODY, width=6)
    draw.line([(rx + 6, ry + 28), (rx + 14, ry + 38)], fill=BODY, width=6)
    # shoes
    draw.ellipse([rx - 30, ry + 34, rx - 22, ry + 39], fill=(255, 255, 255), outline=INK, width=1)
    draw.ellipse([rx + 10, ry + 36, rx + 18, ry + 41], fill=(255, 255, 255), outline=INK, width=1)
    # torso leaning forward + shorts
    draw.line([(rx - 2, ry + 7), (rx - 6, ry + 22)], fill=BODY, width=8)
    draw.ellipse([rx - 11, ry + 17, rx - 1, ry + 27], fill=BODY)
    # back arm (swung back, bent)
    draw.line([(rx - 3, ry + 10), (rx - 16, ry + 14)], fill=SKIN, width=5)
    draw.line([(rx - 16, ry + 14), (rx - 20, ry + 5)], fill=SKIN, width=5)
    # front arm (pumping forward, bent)
    draw.line([(rx - 3, ry + 10), (rx + 10, ry + 16)], fill=SKIN, width=5)
    draw.line([(rx + 10, ry + 16), (rx + 5, ry + 25)], fill=SKIN, width=5)
    # head with hair + headband
    draw.ellipse([rx - 7, ry - 7, rx + 7, ry + 7], fill=SKIN, outline=INK, width=1)
    draw.pieslice([rx - 7, ry - 7, rx + 7, ry + 1], 180, 360, fill=(20, 16, 12))
    draw.line([(rx - 7, ry - 3), (rx + 7, ry - 3)], fill=BRICK, width=2)
    # finish tape
    draw.line([(x + w - 30, y + 6), (x + w - 30, y + h - 20)], fill=INK, width=2)
    for i in range(6):
        draw.rectangle([x + w - 34, y + 8 + i * 7, x + w - 26, y + 11 + i * 7],
                       fill=(0, 0, 0) if i % 2 == 0 else (255, 255, 255))
    # BANNED stamp — top right of the illustration, clear of the tape and headline
    f = SANS_B(9)
    t = "BANNED"
    tw = draw.textlength(t, font=f)
    draw.rectangle([x + w - tw - 46, y + 4, x + w - 40, y + 16], outline=BRICK, width=2)
    draw.text((x + w - tw - 42, y + 6), t, font=f, fill=BRICK)


def scene_bars(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 214, 196))
    base = y + h - 10
    vals = [14, 20, 18, 26, 34]
    bw = 22
    for i, v in enumerate(vals):
        bx = x + 18 + i * 32
        draw.rectangle([bx, base - v, bx + bw, base], fill=NAVY if i < 4 else BRICK, outline=INK, width=1)
    f = SANS_B(13)
    # label top-left, clear of every bar (tallest bar tops out at y+4)
    draw.text((x + 8, y + 2), "4.9%", font=f, fill=BRICK)


# ---------------------------------------------------------------- map
def lonlat_to_xy(lon, lat, x, y, w, h):
    # equirectangular: lon -170..190, lat 78..-58
    px = x + (lon + 170) / 360.0 * w
    py = y + (78 - lat) / 136.0 * h
    return px, py


CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 70), (-95, 69), (-85, 66),
     (-80, 62), (-75, 58), (-65, 60), (-60, 52), (-55, 47), (-65, 44),
     (-70, 42), (-74, 39), (-76, 35), (-80, 32), (-81, 26), (-84, 30),
     (-89, 29), (-94, 29), (-97, 26), (-105, 22), (-110, 23), (-114, 29),
     (-120, 34), (-124, 40), (-124, 48), (-130, 54), (-140, 60), (-155, 58),
     (-165, 60), (-168, 66)],
    # Greenland
    [(-58, 64), (-52, 60), (-43, 60), (-32, 68), (-22, 70), (-20, 76),
     (-35, 80), (-55, 80), (-62, 76), (-58, 70), (-58, 64)],
    # South America
    [(-79, 9), (-72, 11), (-62, 10), (-52, 5), (-50, 0), (-44, -3),
     (-35, -8), (-39, -15), (-41, -23), (-48, -28), (-53, -34), (-58, -39),
     (-65, -41), (-68, -50), (-69, -54), (-73, -50), (-73, -40), (-72, -30),
     (-70, -20), (-77, -12), (-80, -5), (-81, 1), (-79, 9)],
    # Europe (simple outer perimeter: west coast up, north coast east,
    # east side down, Mediterranean coast back west)
    [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (0, 51), (4, 53), (8, 55),
     (8, 57), (10, 59), (12, 57), (18, 56), (21, 55), (24, 58), (28, 59),
     (30, 61), (32, 63), (35, 65), (40, 67), (42, 66), (40, 61), (36, 58),
     (32, 55), (30, 51), (28, 47), (26, 44), (23, 42), (20, 44), (18, 42),
     (15, 44), (12, 44), (8, 44), (3, 43), (0, 40), (-2, 37), (-6, 36),
     (-10, 36)],
    # Africa
    [(-6, 35), (0, 36), (10, 37), (11, 34), (20, 32), (30, 31), (32, 31),
     (35, 28), (38, 22), (40, 15), (43, 11), (48, 11), (51, 11), (51, 2),
     (48, -5), (40, -10), (36, -18), (33, -26), (28, -33), (20, -35),
     (16, -29), (12, -18), (13, -10), (9, -1), (9, 4), (0, 5), (-8, 5),
     (-13, 8), (-17, 15), (-17, 21), (-16, 28), (-10, 31), (-6, 35)],
    # Asia (simple outer perimeter: Black Sea east, Arctic coast east,
    # Pacific coast south with a Korea bump, south coast west to the Levant)
    [(26, 38), (28, 42), (33, 46), (38, 47), (44, 47), (50, 48), (55, 52),
     (60, 55), (65, 58), (70, 62), (75, 66), (80, 68), (85, 70), (90, 72),
     (95, 74), (100, 76), (110, 74), (120, 73), (130, 72), (140, 72),
     (150, 70), (160, 68), (170, 66), (178, 65), (170, 62), (162, 58),
     (156, 52), (142, 50), (140, 45), (135, 43), (130, 42), (128, 40),
     (129, 37), (128, 35), (126, 35), (124, 38), (122, 39), (120, 35),
     (122, 31), (120, 28), (116, 23), (110, 20), (108, 12), (105, 9),
     (103, 2), (100, 7), (98, 10), (97, 16), (94, 17), (92, 21), (89, 22),
     (86, 20), (82, 17), (80, 13), (77, 8), (74, 12), (72, 20), (68, 23),
     (66, 25), (61, 25), (57, 26), (54, 26), (52, 28), (50, 29), (48, 30),
     (46, 30), (44, 29), (42, 32), (40, 35), (36, 36), (33, 36), (30, 36),
     (27, 38), (26, 38)],
    # Arabian Peninsula (separate blob: the main Asia polygon only
    # carries its northern edge, so the peninsula would otherwise be sea)
    [(39, 30), (42, 28), (43, 22), (40, 17), (43, 13), (48, 14), (52, 15),
     (55, 17), (58, 21), (57, 25), (54, 26), (51, 27), (50, 29), (48, 30),
     (44, 30), (42, 32), (39, 30)],
    # Australia
    [(114, -22), (114, -30), (115, -35), (120, -34), (124, -33), (129, -32),
     (132, -32), (136, -35), (140, -38), (145, -38), (150, -37), (153, -32),
     (153, -27), (150, -23), (146, -19), (142, -11), (137, -12), (135, -15),
     (132, -12), (129, -15), (126, -14), (122, -17), (118, -20), (114, -22)],
    # small island groups the main polygons skip (UK, Japan, Indonesia, NZ)
    [(-5, 50), (-1, 53), (0, 55), (-1, 57), (-3, 58), (-5, 56), (-5, 52)],
    [(130, 31), (133, 33), (137, 34), (140, 35), (141, 38), (140, 41),
     (137, 39), (133, 35), (130, 33)],
    [(95, 4), (100, 0), (105, -4), (110, -7), (115, -8), (113, -6),
     (107, -4), (101, 1), (96, 5)],
    [(167, -45), (170, -42), (173, -39), (176, -37), (174, -40), (170, -43)],
]

PINS = [
    (1, 112, 23), (2, 5, 52), (3, 31, 36), (4, 34, 45), (5, 47, 25),
    (6, 84, 21), (7, 127, 37), (8, -45, 64), (9, -74, 41), (10, -118, 34),
    (11, -74, 5), (12, 37, -1), (13, 149, -35),
]

# Badge offsets (px, relative to the pin's true map point) for pins whose
# badges would otherwise overlap a neighbour: 1 Shenzhen/7 Seoul,
# 3 Antalya/4 Kerch/5 Riyadh. A leader line joins badge to true point.
PIN_OFFSETS = {1: (14, 16), 3: (-20, 18), 4: (16, -12)}

BRIEF_DOTS = [
    (24, 57), (20, 55), (15, 50), (-3, 40), (48, 15), (10, 51), (139, 35),
    (-3, 53), (78, 21), (-95, 38), (175, -38), (110, -6), (-69, -23),
    (17, 27), (45, 24), (-98, 39), (46, 5), (-52, -10), (127, 36),
]


def draw_map(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=SEA, outline=INK, width=1)
    for poly in CONTINENTS:
        pts = [lonlat_to_xy(lon, lat, x, y, w, h) for lon, lat in poly]
        draw.polygon(pts, fill=(228, 214, 182), outline=(140, 128, 95))
    for lon, lat in BRIEF_DOTS:
        px, py = lonlat_to_xy(lon, lat, x, y, w, h)
        draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=GREY)
    # leader lines + true-point dots first, badges on top
    for n, lon, lat in PINS:
        px, py = lonlat_to_xy(lon, lat, x, y, w, h)
        dx, dy = PIN_OFFSETS.get(n, (0, 0))
        if (dx, dy) != (0, 0):
            draw.line([(px, py), (px + dx, py + dy)], fill=BRICK, width=2)
            draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=BRICK,
                         outline=(255, 255, 255), width=1)
    for n, lon, lat in PINS:
        px, py = lonlat_to_xy(lon, lat, x, y, w, h)
        dx, dy = PIN_OFFSETS.get(n, (0, 0))
        cx, cy = px + dx, py + dy
        d = 22
        draw.ellipse([cx - d / 2, cy - d / 2, cx + d / 2, cy + d / 2],
                     fill=BRICK, outline=(255, 255, 255), width=2)
        s = str(n)
        f = SANS_B(13 if len(s) < 2 else 12)
        tw = draw.textlength(s, font=f)
        draw.text((cx - tw / 2, cy - 7), s, font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------- content
HEROES = [
    dict(num=1, kicker="SHENZHEN \u00b7 SUMMIT",
         headline="Trump, Xi and Putin share one table",
         deck="First trilateral of the three leaders \u2014 90 minutes at Kylin Villa. "
              "Joint \u2018Declaration Towards Peace\u2019: nuclear war \u2018cannot be won\u2019.",
         source="Reuters \u00b7 AP \u00b7 Xinhua", scene=hero_apec),
    dict(num=2, kicker="THE HAGUE \u00b7 WORLD COURT",
         headline="Myanmar guilty of genocide",
         deck="World Court rules 9\u20136 \u2014 the first state found guilty of genocide "
              "in its 80 years. Reparations and return of refugees ordered.",
         source="Al Jazeera \u00b7 UN News", scene=hero_icj),
    dict(num=3, kicker="ANTALYA \u00b7 CLIMATE",
         headline="COP31 draft drops fossil fuels",
         deck="Slimmer draft text cuts the $120bn adaptation aid goal. "
              "Talks due to end Friday.",
         source="Reuters \u00b7 AFP", scene=hero_cop31),
]

CARDS = [
    dict(num=4, kicker="CRIMEA \u00b7 WAR", headline="Ukraine hits Kerch Bridge again",
         deck="Strike halts trains hours before the APEC summit.",
         source="Reuters", scene=scene_bridge, tag="CLAIM"),
    dict(num=5, kicker="RIYADH \u00b7 WAR", headline="Saudis shoot down Houthi missiles",
         deck="Air defences intercept Houthi missiles over the Saudi capital.",
         source="Reuters \u00b7 AFP", scene=scene_riyadh, tag="CLAIM"),
    dict(num=6, kicker="ODISHA \u00b7 STORM", headline="Cyclone Akvan nears India\u2019s coast",
         deck="Severe storm approaches the east coast; Odisha evacuates 120,000. Landfall due Friday.",
         source="Reuters", scene=scene_cyclone),
    dict(num=7, kicker="SEOUL \u00b7 JUSTICE", headline="Court clears ex-PM Han",
         deck="Top court clears former prime minister Han in a retrial.",
         source="AP", scene=scene_court),
    dict(num=8, kicker="GREENLAND \u00b7 SECURITY", headline="Denmark backs Arctic pact, 109\u20130",
         deck="Parliament votes unanimously for the Arctic pact with the US.",
         source="Reuters", scene=scene_arctic),
    dict(num=9, kicker="NEW YORK \u00b7 MARKETS", headline="Anthropic lists; shares jump 17%",
         deck="Record $81.3bn IPO debuts on Nasdaq and closes at $97.17 \u2014 the biggest listing ever.",
         source="Reuters", scene=scene_stocks),
    dict(num=10, kicker="WORLDWIDE \u00b7 GAMES", headline="GTA VI goes on sale after 13 years",
         deck="Vice City opens at midnight; 99 on Metacritic, $79.99.",
         source="Rockstar \u00b7 press", scene=scene_gta),
    dict(num=11, kicker="BOGOT\u00c1 \u00b7 LABOUR", headline="Unions hold national strike",
         deck="Paro nacional disrupts cities across Colombia.",
         source="Reuters", scene=scene_strike),
    dict(num=12, kicker="NAIROBI \u00b7 SPORT", headline="Marathon champion banned 3 years",
         deck="Jepchirchir suspended for doping.",
         source="AP", scene=scene_runner),
    dict(num=13, kicker="CANBERRA \u00b7 ECONOMY", headline="Jobless rate hits 4.9%",
         deck="Australia\u2019s jobless rate rises to 4.9%.",
         source="ABC", scene=scene_bars),
]

BRIEFS = [
    (14, "GOLD", "Slides to $3,757/oz, lowest since Sept 2025.", "Reuters"),
    (15, "FINLAND", "Approves Onkalo, world\u2019s first nuclear waste store.", "Reuters"),
    (16, "ESTONIA", "Plans to shut Russia border crossings from Dec.", "Reuters"),
    (17, "CZECHIA", "Huge Prague protest for media independence.", "AP"),
    (18, "SPAIN", "General strike disrupts ports and factories.", "Reuters"),
    (19, "YEMEN", "Houthi rocket kills 53 soldiers at army camp.", "Reuters"),
    (20, "GERMANY", "Russian arrested for spying on US firm Palantir.", "AP"),
    (21, "INDIA\u2013JAPAN", "2+2 defence talks open in Tokyo.", "Reuters"),
    (22, "WELLINGTON", "Court: pay equity cuts broke rights law.", "RNZ"),
    (23, "INDIA", "\u2018Ramayana\u2019 crosses \u20b91,000 crore in 14 days.", "AP"),
    (24, "UK", "MAIB: Bayesian had unrecognised wind vulnerability.", "gov.uk"),
    (25, "AUCKLAND", "GTA VI unlocks at midnight.", "RNZ"),
    (26, "JAKARTA", "Asset law passed in parliament.", "Reuters"),
    (27, "ATACAMA", "NASA spots desert bloom from space.", "NASA"),
    (28, "PRETORIA", "Central bank holds rate at 7.25%.", "SABC"),
    (29, "CLIMATE", "Nearly all coral reefs face extinction in 50 years.", "Nature"),
    (30, "LIBYA", "Cocaine and millions of pills seized in the east.", "Reuters"),
    (31, "SAUDI ARABIA", "Danger passed in three southern cities.", "Reuters"),
    (32, "USA", "Senators warn AI cyber threats outpace defences.", "AP"),
    (33, "SOMALIA", "Expels UAE envoy.", "Reuters"),
    (34, "BRAZIL", "Lula backs shorter work week, 44 \u2192 42 hours.", "Reuters"),
    (35, "SOUTH KOREA", "Exports pass $1 trillion.", "Reuters"),
]

REGIONS = [
    ("ASIA 7", BRICK), ("MIDDLE EAST 3", (122, 74, 31)), ("EUROPE 9", NAVY),
    ("AFRICA 4", (60, 120, 70)), ("AMERICAS 6", (110, 70, 140)),
    ("OCEANIA 3", (24, 96, 92)), ("GLOBAL 3", GREY),
]

NUMBERS = [
    ("3", "presidents at one table"),
    ("9\u20136", "World Court vote"),
    ("$81.3bn", "record IPO"),
    ("109\u20130", "Arctic pact vote"),
    ("4.9%", "Australian jobless rate"),
    ("$120bn", "COP31 aid goal cut"),
]

DATE_CHECK = (
    "DATE CHECK \u2713  Every story on this page happened, or was first reported, "
    "on Thursday 19 November 2026.  LEFT OUT AS OTHER DAYS\u2019 NEWS \u2014 18 NOV: "
    "Van Gogh $190.4m sale \u00b7 Jeffries named for Speaker \u00b7 Voyager 1 one "
    "light-day \u00b7 EU \u20ac45bn Ukraine loan \u00b7 Nvidia results \u00b7 Pew 2035 \u00b7 "
    "Anthropic IPO pricing ($83) \u00b7 Gaza push began \u00b7 Carney on China ties \u00b7 "
    "Fed minutes.  NOT YET \u2014 20 NOV: COP31 close \u00b7 "
    "Cyclone Akvan landfall."
)

LEGEND = (
    "HOW SURE ARE WE?  REPORTED = confirmed by named sources \u00b7 CLAIM = one side "
    "says so, unverified \u00b7 FORECAST = a draft, poll or due date \u00b7 DISPUTED = "
    "sources disagree."
)

SOURCES_LINE = (
    "Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 BBC \u00b7 Al Jazeera \u00b7 UN News \u00b7 "
    "ABC \u00b7 RNZ \u00b7 Xinhua \u00b7 Nature \u00b7 NASA \u00b7 2026-11-19. Original drawings."
)


def main():
    img = Image.new("RGB", (W, H), CREAM)
    _IMG[0] = img
    d = ImageDraw.Draw(img)
    X0, X1 = 10, 1014
    CW = X1 - X0

    # ---- kicker line
    y = 8
    d.text((X0, y), "THE WORLD IN ONE DAY", font=SANS_B(13), fill=BRICK)
    r = "35 STORIES \u00b7 7 REGIONS \u00b7 ONE DAY"
    d.text((X1 - d.textlength(r, font=SANS_B(13)), y), r, font=SANS_B(13), fill=NAVY)

    # ---- masthead navy band
    y = 26
    d.rectangle([X0, y, X1, y + 56], fill=NAVY)
    d.rectangle([X0, y + 56, X1, y + 59], fill=GOLD)
    f = SERIF_B(43)
    t = "Thursday 19 November 2026"
    d.text(((W - d.textlength(t, font=f)) / 2, y + 6), t, font=f, fill=(255, 255, 255))

    # ---- subhead
    y = 92
    f = SERIF_I(17)
    t = ("Three presidents meet in Shenzhen \u00b7 The World Court rules on genocide "
         "\u00b7 COP31\u2019s draft drops fossil fuels")
    d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=BRICK)

    # ---- region strip
    y = 112
    f = SANS_B(11)
    widths = [d.textlength(lbl, font=f) + 20 for lbl, _ in REGIONS]
    gap = 6
    extra = (CW - sum(widths) - gap * (len(REGIONS) - 1)) / len(REGIONS)
    cx = X0
    for (lbl, col), wd in zip(REGIONS, widths):
        wd += extra
        d.rectangle([cx, y, cx + wd, y + 18], fill=col)
        d.text((cx + (wd - d.textlength(lbl, font=f)) / 2, y + 3), lbl, font=f,
               fill=(255, 255, 255))
        cx += wd + gap

    # ---- numbers strip (bigger, bolder: rank 1 wins 300px on big stat numbers)
    y = 133
    cell = CW / 6
    for i, (num, lbl) in enumerate(NUMBERS):
        x = X0 + i * cell
        f1 = SERIF_B(26)
        d.text((x + (cell - d.textlength(num, font=f1)) / 2, y), num, font=f1,
               fill=BRICK if i % 2 == 0 else NAVY)
        f2 = SANS_B(10)
        d.text((x + (cell - d.textlength(lbl, font=f2)) / 2, y + 30), lbl, font=f2, fill=INK)
        if i:
            d.line([(x, y + 2), (x, y + 41)], fill=(180, 170, 145), width=1)
    hline(d, X0, X1, y + 44, fill=INK, w=1)

    # ---- hero panels
    y = 180
    PH, PW = 226, 329
    for i, hero in enumerate(HEROES):
        x = X0 + i * (PW + 8)
        card_frame(d, x, y, PW, PH)
        hero["scene"](d, x + 1, y + 1, PW - 2, 116)
        ty = y + 120
        badge_num(d, x + 8, ty + 1, hero["num"], 17)
        d.text((x + 30, ty + 2), hero["kicker"], font=SANS_B(10), fill=BRICK)
        hl = wrap(d, hero["headline"], SERIF_B(18), PW - 16)
        ty2 = text_block(d, x + 8, ty + 16, hl, SERIF_B(18), INK, leading=19)
        dk = wrap(d, hero["deck"], SANS(10), PW - 16)
        ty3 = text_block(d, x + 8, ty2 + 1, dk, SANS(10), INK, leading=11)
        d.text((x + 8, y + PH - 14), hero["source"], font=SANS(9), fill=GREY)
        tag(d, x + PW - 74, y + PH - 15, "REPORTED")

    # ---- secondary grid 2 x 5
    y = 410
    RH, CWd = 146, 194
    for r in range(2):
        for c in range(5):
            card = CARDS[r * 5 + c]
            x = X0 + c * (CWd + 8)
            yy = y + r * (RH + 8)
            card_frame(d, x, yy, CWd, RH)
            card["scene"](d, x + 1, yy + 1, CWd - 2, 48)
            ty = yy + 52
            badge_num(d, x + 6, ty, card["num"], 15)
            d.text((x + 25, ty + 1), card["kicker"], font=SANS_B(9), fill=BRICK)
            hl = wrap(d, card["headline"], SERIF_B(14), CWd - 12)
            ty2 = text_block(d, x + 6, ty + 15, hl[:2], SERIF_B(14), INK, leading=15)
            dk = wrap(d, card["deck"], SANS(10), CWd - 12)
            text_block(d, x + 6, ty2 + 1, dk[:3], SANS(10), INK, leading=11)
            d.text((x + 6, yy + RH - 13), card["source"], font=SANS(8), fill=(64, 60, 52))
            tag(d, x + CWd - 66, yy + RH - 14, card.get("tag", "REPORTED"))

    # ---- bottom: map + briefs
    y = 714
    d.text((X0, y), "WHERE IT HAPPENED", font=SANS_B(12), fill=INK)
    d.text((X0, y + 13), "Red numbers mark stories 1\u201313; grey dots mark the briefs below.",
           font=SANS(8), fill=GREY)
    map_w, map_h = 320, 150
    draw_map(d, X0, y + 24, map_w, map_h)

    bx = X0 + map_w + 8
    bw = X1 - bx
    d.text((bx, y), "ALSO ON THURSDAY 19 NOVEMBER 2026", font=SANS_B(12), fill=INK)
    d.text((bx, y + 13), "place \u00b7 what happened \u00b7 source", font=SANS_O(8), fill=GREY)
    col_w = (bw - 8) / 2
    # 9pt briefs: the wider map narrows the columns, and 10pt briefs
    # would spill 70px past the DATE CHECK box; 9pt still reads cleanly
    # at full size (briefs are not a 300px element anyway).
    f_b, f_r = SANS_B(9), SANS(9)
    for ci in range(2):
        col_items = BRIEFS[ci * 11:(ci + 1) * 11]
        yy = y + 22
        cx0 = bx + ci * (col_w + 8)
        for num, place, text, src in col_items:
            num_s = "%d " % num
            head = "%s \u2014 " % place
            rest = "%s (%s)" % (text, src)
            # wrap rest to fit under head on first line, then full width
            first_w = col_w - d.textlength(num_s + head, font=f_b)
            lines = wrap(d, rest, f_r, first_w)
            d.text((cx0, yy), num_s, font=f_b, fill=BRICK)
            nx = cx0 + d.textlength(num_s, font=f_b)
            d.text((nx, yy), head, font=f_b, fill=INK)
            d.text((nx + d.textlength(head, font=f_b), yy), lines[0], font=f_r, fill=INK)
            yy += 11
            for ln in lines[1:]:
                d.text((cx0, yy), ln, font=f_r, fill=INK)
                yy += 11

    # ---- footer: DATE CHECK box
    y = 894
    d.rectangle([X0, y, X1, y + 60], outline=BRICK, width=2)
    f = SANS(10)
    lines = wrap(d, DATE_CHECK, f, CW - 20)
    text_block(d, X0 + 10, y + 6, lines, f, INK, leading=13)

    # ---- legend + sources
    y = 962
    f = SANS(9)
    lines = wrap(d, LEGEND, f, CW)
    y = text_block(d, X0, y, lines, f, INK, leading=12)
    d.text((X0, y + 4), SOURCES_LINE, font=SANS(9), fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size, os.path.getsize("entry.png"), "bytes")


if __name__ == "__main__":
    main()
