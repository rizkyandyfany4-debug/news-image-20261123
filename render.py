#!/usr/bin/env python3
"""Render the 23 November 2026 front page: THE WORLD IN ONE IMAGE.
Deterministic: no timestamps, no randomness, fixed layout and fonts.
Writes entry.png (1024x1024) next to this script."""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 48
INK = (17, 17, 17)
RED = (139, 0, 0)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Word-wrap text to fit max_w pixels. Returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, text, fnt, x, y, max_w, fill=INK, leading=None):
    """Draw wrapped text starting at (x, y). Returns y after the last line."""
    lh = leading if leading is not None else int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def rule(draw, y, x0, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)
    return y + width


def main():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    x0, x1 = MARGIN, W - MARGIN
    content_w = x1 - x0

    # ---------- Masthead ----------
    y = 34
    f_mast = font(SERIF_B, 58)
    title = "THE WORLD IN ONE IMAGE"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, y), title, font=f_mast, fill=INK)
    y += 72
    f_date = font(SANS_B, 25)
    date = "M O N D A Y ,  2 3  N O V E M B E R  2 0 2 6"
    tw = d.textlength(date, font=f_date)
    d.text(((W - tw) / 2, y), date, font=f_date, fill=INK)
    y += 44
    y = rule(d, y, x0, x1, 3)
    y = rule(d, y + 4, x0, x1, 1)
    y += 16

    # ---------- Lead story ----------
    f_kick = font(SANS_B, 22)
    d.text((x0, y), "UNITED STATES", font=f_kick, fill=RED)
    y += 34
    f_lead = font(SERIF_B, 62)
    d.text((x0, y), "IOWA BRACES", font=f_lead, fill=INK)
    y += 70
    d.text((x0, y), "FOR A BLAST", font=f_lead, fill=INK)
    y += 72
    f_deck = font(SANS, 25)
    y = draw_wrapped(
        d,
        "The US Army plans to detonate tons of unstable explosives at an "
        "Iowa munitions plant today, after a court paused the plan and the "
        "Army invoked emergency powers to proceed.",
        f_deck, x0, y, content_w, leading=30)
    y += 6
    f_sub = font(SERIF, 22)
    y = draw_wrapped(
        d,
        "About 400 residents of Middletown were told to leave as degrading "
        "lead azide, a bomb-making chemical, grows more dangerous in storage.",
        f_sub, x0, y, content_w, leading=26)
    y += 12
    y = rule(d, y, x0, x1, 2)
    y += 10

    # ---------- Two secondary stories ----------
    col_w = (content_w - 36) // 2
    col2_x = x0 + col_w + 36
    top = y

    # Left: Indonesia
    f_k2 = font(SANS_B, 20)
    d.text((x0, top), "INDONESIA", font=f_k2, fill=RED)
    f_h2 = font(SERIF_B, 33)
    yy = top + 32
    yy = draw_wrapped(d, "SEARCH RESUMES AT CIKANDE", f_h2, x0, yy, col_w,
                      leading=40)
    yy += 6
    f_b2 = font(SANS, 21)
    yy = draw_wrapped(
        d,
        "Police pulled 24 body bags from the ruins of a Java candy factory "
        "on Sunday. Twenty-nine workers are still missing as the search "
        "resumes this morning; victims are unidentifiable by sight and DNA "
        "tests could take weeks.",
        f_b2, x0, yy, col_w, leading=24)

    # Right: Markets
    d.text((col2_x, top), "MARKETS", font=f_k2, fill=RED)
    yy2 = top + 32
    yy2 = draw_wrapped(d, "WALL STREET OPENS THE WEEK IN CORRECTION",
                       f_h2, col2_x, yy2, col_w, leading=40)
    yy2 += 6
    yy2 = draw_wrapped(
        d,
        "The S&P 500 fell 3.7% on Friday to 6,910, more than 10% below its "
        "October record, its worst week in 18 months. The Nasdaq lost about "
        "10% for the week.",
        f_b2, col2_x, yy2, col_w, leading=24)

    y = max(yy, yy2) + 12
    y = rule(d, y, x0, x1, 2)
    y += 10

    # ---------- Also strip ----------
    f_also = font(SANS_B, 20)
    d.text((x0, y), "ALSO TODAY", font=f_also, fill=RED)
    y += 26
    items = [
        ("BOX OFFICE — ", "'Sunrise on the Reaping' tops North America with "
         "about $120m in its opening weekend."),
        ("TRAVEL — ", "A calmer Monday for Thanksgiving flyers after the "
         "weekend's nationwide FAA ground stop; some Northeast delays may "
         "linger."),
        ("MANILA — ", "The Philippines opens Asia-Pacific farm "
         "modernisation talks in Para\u00f1aque, running to Thursday."),
        ("WEATHER — ", "Storms are due in the US South and West Coast on "
         "Tuesday; a major Northeast storm may strike on Thanksgiving Day."),
    ]
    f_item_b = font(SANS_B, 18)
    f_item = font(SANS, 18)
    half = (content_w - 36) // 2
    col_y = [y, y]
    for i, (lead, rest) in enumerate(items):
        col = i % 2
        xx = x0 if col == 0 else col2_x
        cy = col_y[col]
        # bold lead-in then regular text, wrapped as one paragraph
        full = lead + rest
        # draw wrapped lines, bolding only the lead-in on the first line
        lines = wrap(d, full, f_item, half)
        lh = 22
        for li, line in enumerate(lines):
            if li == 0 and line.startswith(lead):
                d.text((xx, cy), lead, font=f_item_b, fill=INK)
                d.text((xx + d.textlength(lead, font=f_item_b), cy),
                       line[len(lead):], font=f_item, fill=INK)
            else:
                d.text((xx, cy), line, font=f_item, fill=INK)
            cy += lh
        col_y[col] = cy + 8
    y = max(col_y) + 4
    y = rule(d, y, x0, x1, 1)
    y += 8

    # ---------- Footer ----------
    f_foot = font(SANS, 15)
    foot = "Sources: Reuters, AP, AFP  •  Monday, 23 November 2026"
    tw = d.textlength(foot, font=f_foot)
    d.text(((W - tw) / 2, y), foot, font=f_foot, fill=GREY)

    print("footer y:", y)
    assert y + 20 <= H, f"layout overflow: footer at {y}"
    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
    print("rendered entry.png")
