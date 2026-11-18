"""MARIN.EXE Digital Scrapbook asset builder.

Run from repository root:
    python tools/build_assets.py

Regenerates every decorative SVG in assets/ as a cut-and-paste scrapbook:
kraft paper, washi tape, torn paper, sticky notes, polaroid frames,
wax seals, coffee stains and handwritten journaling. All SMIL animation is
dropped so the assets render as static images everywhere.

The supplied profile-picture.svg is deliberately never touched.
"""
from __future__ import annotations

import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")
os.makedirs(OUT, exist_ok=True)
W = 924

PAPER = "#FBF7EE"
KRAFT = "#EADCC9"
INK = "#3C3C3C"
EMERALD = "#157A5E"
MINT = "#C1EAD5"
PINK = "#FEC9CB"
LAV = "#E5D7FC"
BLUSH = "#FBE4E8"
CREAM = "#FFF8DC"
GOLD = "#EAC05A"
STITCH = "#9B8672"
WHITE = "#FFFFFF"
HAND = "'Comic Sans MS', 'Segoe Script', 'Chalkboard SE', cursive"
BODY = "'Trebuchet MS', Arial, sans-serif"
DISPLAY = "'Comic Sans MS', 'Marker Felt', 'Chalkboard SE', cursive"


def svg(w, h, body, label):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{label}">'
        f'<title>{label}</title>{defs()}{body}</svg>'
    )


def save(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)


def defs():
    return (
        '<defs>'
        '<filter id="drop" x="-25%" y="-25%" width="150%" height="150%">'
        '<feDropShadow dx="5" dy="7" stdDeviation="8" flood-color="#000" flood-opacity=".16"/></filter>'
        '<filter id="dropSm" x="-15%" y="-15%" width="130%" height="130%">'
        '<feDropShadow dx="3" dy="4" stdDeviation="5" flood-color="#000" flood-opacity=".13"/></filter>'
        '<filter id="blur"><feGaussianBlur stdDeviation="22"/></filter>'
        '<pattern id="speckle" width="44" height="44" patternUnits="userSpaceOnUse">'
        '<circle cx="7" cy="9" r="1" fill="#C9B691" opacity=".3"/>'
        '<circle cx="33" cy="35" r="1" fill="#C9B691" opacity=".25"/>'
        '<circle cx="20" cy="39" r="1" fill="#C9B691" opacity=".2"/></pattern>'
        '<pattern id="ruled" width="26" height="26" patternUnits="userSpaceOnUse">'
        '<path d="M0 25H26" fill="none" stroke="#E7CFA2" stroke-width="1" stroke-opacity=".5"/></pattern>'
        '<linearGradient id="coffee" x1="0" y1="0" x2="1" y2="1">'
        '<stop stop-color="#8D6E63" stop-opacity=".5"/><stop offset="1" stop-color="#8D6E63" stop-opacity="0"/></linearGradient>'
        '</defs>'
    )


def torn_path(x, y, w, h, amp=14, seed=0):
    rr = random.Random(seed)
    pts = [f"M{x} {y}"]
    nx = x
    while nx < x + w - 6:
        step = rr.uniform(11, 23)
        nx = min(nx + step, x + w - 6)
        pts.append(f"L{nx:.1f} {y + rr.uniform(1, amp):.1f}")
    pts.append(f"L{x + w} {y}")
    pts.append(f"L{x + w} {y + h}")
    pts.append(f"L{x} {y + h}")
    pts.append("Z")
    return " ".join(pts)


def stitch(x, y, w, h, color=STITCH):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" '
        f'stroke="{color}" stroke-width="1.6" stroke-dasharray="2.5 3" stroke-linecap="round"/>'
    )


def washi(x, y, w, h, color=PINK, radius=10):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{color}" filter="url(#drop)"/>'
        f'<path d="M{x} {y + 5} H{x + w}" fill="none" stroke="#000000" stroke-width="1" '
        f'stroke-opacity=".10" stroke-dasharray="4 2" stroke-linecap="round"/>'
        f'<path d="M{x} {y + h - 5} H{x + w}" fill="none" stroke="#FFFFFF" stroke-width="1.2" '
        f'stroke-dasharray="4 2" stroke-linecap="round"/>'
    )


def sticky(x, y, size, color, rot, text, tcolor=INK, ts=17, seed=0):
    cx = x + size / 2
    cy = y + size / 2
    return (
        f'<g transform="rotate({rot} {cx:.1f} {cy:.1f})" filter="url(#drop)">'
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{size:.1f}" height="{size:.1f}" rx="6" fill="{color}"/>'
        f'<path d="M{x + 2:.1f} {y + 2:.1f} L{x + size - 2:.1f} {y + 2:.1f}" fill="none" '
        f'stroke="#FFFFFF" stroke-width="1.2" stroke-opacity=".55" stroke-linecap="round"/>'
        f'<path d="M{x + 2:.1f} {y + size - 2:.1f} L{x + size - 2:.1f} {y + size - 2:.1f}" fill="none" '
        f'stroke="#000000" stroke-width="1.2" stroke-opacity=".12" stroke-linecap="round"/>'
        f'<text x="{cx:.1f}" y="{cy + ts / 2.6:.1f}" font-family="{HAND}" font-size="{ts}" '
        f'fill="{tcolor}" text-anchor="middle">{text}</text>'
        f'</g>'
    )


def pin(cx, cy, color=EMERALD):
    return (
        f'<circle cx="{cx}" cy="{cy}" r="4" fill="{color}" filter="url(#dropSm)"/>'
        f'<rect x="{cx - 0.7}" y="{cy - 4}" width="1.4" height="4" fill="#FFFFFF"/>'
    )


def seal(cx, cy, r_, text, color=EMERALD, tcolor=WHITE):
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r_}" fill="{color}" filter="url(#drop)"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r_ - 3}" fill="none" stroke="#FFFFFF" stroke-width="2" '
        f'stroke-opacity=".7" stroke-dasharray="2 3"/>'
        f'<text x="{cx}" y="{cy + 5}" font-family="{BODY}" font-size="12" font-weight="700" '
        f'fill="{tcolor}" text-anchor="middle">{text}</text>'
    )


def heart(cx, cy, s, color=PINK):
    return (
        f'<path d="M{cx - s/2:.1f} {cy:.1f}Q{cx - s/2:.1f} {cy - s/2:.1f} {cx:.1f} {cy - s/4:.1f}Q'
        f'{cx + s/2:.1f} {cy - s/2:.1f} {cx + s/2:.1f} {cy:.1f}Q{cx + s/2:.1f} {cy + s/2:.1f} '
        f'{cx:.1f} {cy + s:.1f} {cx - s/2:.1f} {cy:.1f}Z" fill="{color}" opacity=".9" filter="url(#dropSm)"/>'
    )


def marquee() -> None:
    b = f'<rect width="{W}" height="72" fill="{PAPER}"/>'
    b += f'<rect width="{W}" height="72" fill="url(#speckle)"/>'
    b += washi(0, 20, W, 32, PINK)
    b += f'<text x="{W/2:.1f}" y="46" font-family="{DISPLAY}" font-size="21" fill="{INK}" text-anchor="middle">marin.exe  ·  digital scrapbook  ·  2026</text>'
    b += heart(44, 52, 11) + heart(W - 44, 52, 11)
    b += f'<ellipse cx="{W*0.8}" cy="12" rx="40" ry="18" fill="url(#coffee)" filter="url(#blur)"/>'
    save("marquee.svg", svg(W, 72, b, "marin.exe digital scrapbook washi header"))


def banner() -> None:
    b = f'<rect width="{W}" height="460" fill="{KRAFT}"/>'
    b += f'<rect width="{W}" height="460" fill="url(#speckle)"/>'
    b += f'<ellipse cx="120" cy="384" rx="46" ry="28" fill="url(#coffee)" filter="url(#blur)"/>'
    b += f'<ellipse cx="805" cy="52" rx="52" ry="30" fill="url(#coffee)" filter="url(#blur)"/>'
    b += f'<path d="{torn_path(34, 44, 470, 152, seed=1)}" fill="{PAPER}" filter="url(#drop)"/>'
    b += f'<text x="62" y="86" font-family="{DISPLAY}" font-size="33" fill="{INK}">cosplay my code</text>'
    b += f'<text x="62" y="126" font-family="{HAND}" font-size="24" fill="{EMERALD}">make it perfect.</text>'
    b += f'<text x="62" y="166" font-family="{BODY}" font-size="15" fill="{INK}" opacity=".7">digital scrapbook · vol. 001</text>'
    b += f'<g filter="url(#drop)" transform="translate(620, 56)">'
    b += f'<rect width="272" height="318" rx="6" fill="{WHITE}"/>'
    b += f'<rect x="26" y="26" width="220" height="220" rx="4" fill="{CREAM}" stroke="{INK}" stroke-opacity=".15" stroke-width="1"/>'
    b += f'<rect x="26" y="262" width="220" height="30" rx="4" fill="{PAPER}"/>'
    b += f'<text x="136" y="281" font-family="{HAND}" font-size="13" fill="{INK}" text-anchor="middle">marin kitagawa · cosplay queen</text>'
    b += f'</g>'
    b += washi(642, 80, 228, 14, BLUSH)
    b += sticky(38, 240, 104, MINT, -9, "cosplay", ts=17, seed=3)
    b += sticky(160, 268, 96, PINK, 6, "make it", ts=16, seed=4)
    b += sticky(278, 226, 100, LAV, -4, "perfect_", ts=17, seed=5)
    b += seal(816, 358, 26, "EST 2026")
    b += seal(870, 402, 20, "GUR")
    b += f'<path d="{torn_path(34, 362, 420, 66, seed=2)}" fill="{CREAM}" filter="url(#drop)"/>'
    b += f'<text x="62" y="404" font-family="{HAND}" font-size="16" fill="{INK}">digital memories · scrapbook vol. 001</text>'
    save("banner.svg", svg(W, 460, b, "marin.exe scrapbook hero banner"))


def card() -> None:
    b = f'<rect width="{W}" height="380" fill="{PAPER}"/>'
    b += f'<rect width="{W}" height="380" fill="url(#ruled)"/>'
    b += f'<ellipse cx="850" cy="338" rx="48" ry="30" fill="url(#coffee)" filter="url(#blur)"/>'
    b += f'<path d="{torn_path(30, 26, 864, 64, seed=3)}" fill="{KRAFT}" filter="url(#drop)"/>'
    b += f'<text x="58" y="66" font-family="{DISPLAY}" font-size="23" fill="{INK}">player journal / 01</text>'
    b += washi(690, 40, 210, 30, BLUSH)
    b += f'<text x="795" y="61" font-family="{HAND}" font-size="15" fill="{INK}" text-anchor="end">connected</text>'
    rows = [
        ("NAME", "Deepanjali Vishwakarma"),
        ("HOMELAND", "Mumbai, Maharashtra, India"),
        ("CLASS", "Frontend Developer"),
        ("SPECIAL ABILITY", "Python · Linux · React · C++"),
    ]
    y = 120
    for label, value in rows:
        b += f'<rect x="52" y="{y-8}" width="200" height="36" rx="8" fill="{PINK}" filter="url(#dropSm)"/>'
        b += f'<text x="62" y="{y+14}" font-family="{HAND}" font-size="15" fill="{INK}">{label}</text>'
        b += f'<rect x="272" y="{y-8}" width="600" height="40" rx="10" fill="{CREAM}" stroke="{STITCH}" stroke-width="1.2" stroke-dasharray="1.4 1.8" stroke-linecap="round" filter="url(#dropSm)"/>'
        b += f'<text x="294" y="{y+16}" font-family="{BODY}" font-size="20" font-weight="700" fill="{INK}">{value}</text>'
        y += 58
    b += seal(836, 350, 24, "LVL ∞")
    b += heart(44, 352, 10) + heart(W - 44, 348, 10)
    b += sticky(670, 150, 72, MINT, 10, "gurly", ts=13, seed=6)
    save("card.svg", svg(W, 380, b, "player journal scrapbook card"))


def skills() -> None:
    b = f'<rect width="{W}" height="230" fill="{PAPER}"/>'
    b += f'<rect width="{W}" height="230" fill="url(#speckle)" opacity=".6"/>'
    notes = [
        (38, 34, 110, MINT, -7, "HTML5", 18),
        (260, 34, 100, PINK, 5, "CSS3", 17),
        (482, 34, 104, LAV, -4, "JavaScript", 17),
        (704, 34, 96, MINT, 8, "React", 17),
        (162, 146, 100, BLUSH, -6, "Liquid", 17),
        (384, 146, 108, "#C9AED5", 4, "Python", 17),
        (606, 146, 92, GOLD, -9, "C++", 17),
        (828, 146, 86, PINK, 6, "Git", 15),
    ]
    for x, y, size, color, rot, text, ts in notes:
        b += sticky(x, y, size, color, rot, text, ts=ts, seed=len(text))
        b += pin(x + size / 2, y - 14)
    save("skills.svg", svg(W, 230, b, "Technology stack scrapbook sticky notes"))


def heading(name, title, label, right=False) -> None:
    b = f'<rect width="{W}" height="112" fill="{PAPER}"/>'
    b += f'<rect width="{W}" height="112" fill="url(#speckle)" opacity=".5"/>'
    width = min(760, max(300, len(title) * 15 + 100))
    x = W - width - 34 if right else 34
    b += f'<path d="{torn_path(x, 22, width, 68, seed=4)}" fill="{KRAFT}" filter="url(#drop)"/>'
    b += stitch(x, 22, width, 68)
    anchor = "end" if right else "start"
    tx = x + width - 26 if right else x + 26
    b += f'<text x="{tx}" y="72" font-family="{HAND}" font-size="26" fill="{INK}" text-anchor="{anchor}">{title}</text>'
    b += heart(x - 18 if right else x + width + 18, 58, 13)
    b += pin(x + width / 2, 12) + pin(x + width / 2, 100)
    save(name, svg(W, 112, b, label))


def button(name, title, url_label) -> None:
    b = f'<rect width="308" height="124" fill="{PAPER}"/>'
    b += f'<rect width="308" height="124" fill="url(#speckle)"/>'
    b += f'<rect x="14" y="10" width="280" height="104" rx="10" fill="{WHITE}" stroke="{INK}" stroke-width="1" stroke-dasharray="3 3" stroke-linecap="round" filter="url(#drop)"/>'
    b += f'<text x="154" y="62" font-family="{DISPLAY}" font-size="27" fill="{EMERALD}" text-anchor="middle">{title}</text>'
    b += f'<text x="154" y="92" font-family="{BODY}" font-size="12" fill="{INK}" text-anchor="middle" opacity=".6">{url_label}</text>'
    b += heart(34, 100, 10) + heart(274, 100, 10)
    save(name, svg(308, 124, b, url_label))


def footer() -> None:
    b = f'<rect width="{W}" height="196" fill="{PAPER}"/>'
    b += f'<rect width="{W}" height="196" fill="url(#speckle)"/>'
    b += washi(0, 18, W, 26, MINT)
    b += f'<text x="{W/2:.1f}" y="82" font-family="{HAND}" font-size="25" fill="{INK}" text-anchor="middle">gurly’s journey continues…</text>'
    b += f'<text x="{W/2:.1f}" y="120" font-family="{DISPLAY}" font-size="29" fill="{EMERALD}" text-anchor="middle">level up never ends!</text>'
    b += heart(76, 152, 12) + heart(W - 76, 152, 12)
    b += f'<ellipse cx="{W*0.86}" cy="24" rx="36" ry="16" fill="url(#coffee)" filter="url(#blur)"/>'
    b += sticky(34, 148, 76, BLUSH, 8, "keep", ts=13, seed=7)
    b += sticky(W - 110, 148, 76, PINK, -6, "going", ts=13, seed=8)
    save("footer.svg", svg(W, 196, b, "gurly's journey continues level up never ends"))


def main() -> None:
    marquee()
    banner()
    card()
    skills()
    heading("h-snake.svg", "WATCH THE SNAKE EAT MY CONTRIBUTIONS", "Watch the snake eat my contributions")
    heading("h-connect.svg", "LET’S CONNECT", "Let's connect", right=True)
    button("btn-email.svg", "EMAIL", "Email")
    button("btn-github.svg", "GITHUB", "GitHub")
    button("btn-instagram.svg", "INSTAGRAM", "Instagram")
    footer()
    print("Digital scrapbook SVG assets generated. profile-picture.svg was preserved.")


if __name__ == "__main__":
    main()
