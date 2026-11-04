"""MARIN.EXE asset builder.

Usage (from the repo root):
    python tools/build_assets.py              # uses ./marin.jpg if it exists, else a placeholder frame
    python tools/build_assets.py path/to/photo.jpg

Writes SVG tiles into ./assets. Pillow is optional (resizes the photo so the SVG stays small).
"""
import base64
import io
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "assets")
os.makedirs(OUT, exist_ok=True)

W = 924
INK = "#17131F"
HOT = "#FF69B4"
BUB = "#FFB6C1"
CREAM = "#FFF4E6"
LAV = "#CDB4DB"
PURPLE = "#9D4EDD"
PEACH = "#FFD6A5"
DISPLAY = "'Arial Black',Impact,'Helvetica Neue',Arial,sans-serif"
BODY = "'Trebuchet MS',Arial,sans-serif"
MONO = "'Courier New',Consolas,monospace"
SW = 8


def svg(w, h, body, label, bg=CREAM, defs=""):
    base = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">'
            f"<title>{label}</title>{defs}{base}{body}</svg>")


def text(x, y, s, size, fill=INK, anchor="start", weight=900, font=DISPLAY,
         tl=None, stroke=None, sw=0):
    a = f' textLength="{tl}" lengthAdjust="spacingAndGlyphs"' if tl else ""

    def one(f, extra=""):
        return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" '
                f'font-weight="{weight}" fill="{f}" text-anchor="{anchor}"{a}{extra}>{s}</text>')
    if stroke:
        back = one(stroke, f' stroke="{stroke}" stroke-width="{sw * 2}" stroke-linejoin="round"')
        return back + one(fill)
    return one(fill)


def box(x, y, w, h, fill, sw=SW, off=14, rot=0, shadow=INK):
    tr = f' transform="rotate({rot} {x + w / 2} {y + h / 2})"' if rot else ""
    return (f"<g{tr}>"
            f'<rect x="{x + off}" y="{y + off}" width="{w}" height="{h}" fill="{shadow}" stroke="{INK}" stroke-width="{sw}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{INK}" stroke-width="{sw}"/>'
            f"</g>")


def burst(cx, cy, r, fill, n=14, rot=0, sh=8, sw=SW):
    def poly(ox, oy, f):
        pts = []
        for i in range(n * 2):
            a = -math.pi / 2 + i * math.pi / n
            rr = r if i % 2 == 0 else r * 0.76
            pts.append(f"{cx + ox + rr * math.cos(a):.1f},{cy + oy + rr * math.sin(a):.1f}")
        return (f'<polygon points="{" ".join(pts)}" fill="{f}" stroke="{INK}" '
                f'stroke-width="{sw}" stroke-linejoin="miter" transform="rotate({rot} {cx} {cy})"/>')
    return (poly(sh, sh, INK) if sh else "") + poly(0, 0, fill)


def heart(cx, cy, s, fill, rot=0, sh=6, sw=SW, shadow=True):
    d = ("M0,-0.35 C0,-1 -1,-1 -1,-0.3 C-1,0.25 -0.3,0.6 0,1 "
         "C0.3,0.6 1,0.25 1,-0.3 C1,-1 0,-1 0,-0.35Z")

    def one(ox, oy, f):
        sk = f' stroke="{INK}" stroke-width="{sw / s:.3f}" stroke-linejoin="round"' if sw else ""
        return (f'<path d="{d}" fill="{f}"{sk} '
                f'transform="translate({cx + ox} {cy + oy}) rotate({rot}) scale({s})"/>')
    return (one(sh, sh, INK) if shadow else "") + one(0, 0, fill)


def sparkle(cx, cy, r, fill, sh=6, sw=6):
    def one(ox, oy, f):
        x, y = cx + ox, cy + oy
        d = (f"M{x},{y - r} Q{x},{y} {x + r},{y} Q{x},{y} {x},{y + r} "
             f"Q{x},{y} {x - r},{y} Q{x},{y} {x},{y - r}Z")
        return f'<path d="{d}" fill="{f}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>'
    return one(sh, sh, INK) + one(0, 0, fill)


def window(x, y, w, h, title, bar, bg=CREAM, off=16, title_fill=INK):
    s = f'<rect x="{x + off}" y="{y + off}" width="{w}" height="{h}" fill="{INK}"/>'
    s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{bg}" stroke="{INK}" stroke-width="{SW}"/>'
    s += f'<rect x="{x}" y="{y}" width="{w}" height="52" fill="{bar}" stroke="{INK}" stroke-width="{SW}"/>'
    for i, c in enumerate([HOT, CREAM, PEACH]):
        s += f'<rect x="{x + 20 + i * 36}" y="{y + 14}" width="24" height="24" fill="{c}" stroke="{INK}" stroke-width="5"/>'
    s += text(x + w - 22, y + 34, title, 21, title_fill, "end", 700, MONO)
    return s


def save(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)


# ---------- marquee ----------
def marquee():
    cyc = 832
    seg = ""
    for i in range(3):
        o = i * cyc
        seg += text(o, 37, "MARIN.EXE", 24, HOT, tl=150)
        seg += burst(o + 184, 28, 14, PEACH, n=8, sh=0, sw=0)
        seg += text(o + 216, 37, "COSPLAY MY CODE", 24, CREAM, tl=250)
        seg += burst(o + 498, 28, 14, PEACH, n=8, sh=0, sw=0)
        seg += text(o + 530, 37, "MAKE IT PERFECT", 24, CREAM, tl=250)
        seg += heart(o + 812, 27, 13, HOT, sh=0, sw=0, shadow=False)
    anim = ('<animateTransform attributeName="transform" type="translate" '
            f'from="0 0" to="-{cyc} 0" dur="16s" repeatCount="indefinite"/>')
    body = (f'<rect width="{W}" height="56" fill="{INK}"/>'
            f'<rect y="0" width="{W}" height="6" fill="{HOT}"/>'
            f'<rect y="50" width="{W}" height="6" fill="{HOT}"/>'
            f"<g>{seg}{anim}</g>")
    save("marquee.svg", svg(W, 56, body, "MARIN.EXE: cosplay my code, make it perfect", bg=None))


# ---------- hero: asymmetrical stacked panels ----------
def banner():
    b = box(24, 30, 568, 366, HOT, sw=SW, off=14)
    lines = [("COSPLAY", 7, True), ("MY CODE,", 8, False), ("MAKE IT", 7, True), ("PERFECT!", 8, False)]
    y = 138
    for s, n, outlined in lines:
        if outlined:
            b += text(52, y, s, 72, CREAM, tl=n * 54, stroke=INK, sw=5)
        else:
            b += text(52, y, s, 72, INK, tl=n * 54)
        y += 76
    b += '<g transform="rotate(-4 139 30)">' + box(44, 8, 190, 44, CREAM, sw=7, off=8)
    b += text(139, 39, "MARIN.EXE", 22, INK, "middle", 700, MONO) + "</g>"
    b += burst(516, 128, 46, PEACH, n=12, rot=8, sw=7)
    b += heart(516, 132, 22, HOT, rot=-8, sh=0, sw=5, shadow=False)
    # right column, offset
    b += box(624, 30, 276, 170, LAV, sw=SW, off=14)
    for i, c in enumerate([HOT, CREAM, PEACH]):
        b += f'<rect x="{644 + i * 36}" y="{50}" width="24" height="24" fill="{c}" stroke="{INK}" stroke-width="5"/>'
    b += text(644, 138, "MARIN.EXE", 46, INK, tl=236)
    b += text(644, 176, "gurly_profile.exe", 19, INK, "start", 700, MONO)
    b += box(600, 232, 300, 164, PEACH, sw=SW, off=14)
    b += text(622, 292, "HERE'S YOUR", 40, INK, tl=246)
    b += text(622, 362, "GURLY!", 66, HOT, tl=196, stroke=INK, sw=5)
    b += sparkle(866, 364, 24, PURPLE, sh=5, sw=6)
    b += sparkle(590, 214, 18, CREAM, sh=4, sw=5)
    save("banner.svg", svg(W, 432, b, "MARIN.EXE. Cosplay my code, make it perfect! Here's your gurly!"))


# ---------- character sheet ----------
def card():
    b = window(22, 22, 868, 312, "player_card.sav", PURPLE, bg=BUB, title_fill=CREAM)
    rows = [("NAME", "Deepanjali Vishwakarma", HOT, INK),
            ("HOMELAND", "Mumbai, Maharashtra, India", PEACH, INK),
            ("CLASS", "Frontend Developer", LAV, INK),
            ("SPECIAL ABILITY", "[Python, Linux, React &amp; C++]", PURPLE, CREAM)]
    y = 94
    for label, val, c, tc in rows:
        tl = 190 if len(label) > 9 else None
        b += box(46, y, 220, 46, c, sw=7, off=8)
        b += text(156, y + 31, label, 19, tc, "middle", 700, MONO, tl=tl)
        b += f'<rect x="288" y="{y}" width="460" height="46" fill="{CREAM}" stroke="{INK}" stroke-width="7"/>'
        b += text(304, y + 32, val, 24, INK, "start", 700, BODY)
        y += 58
    b += burst(826, 196, 60, PEACH, n=12, rot=-6, sw=7)
    b += text(826, 192, "LVL", 21, INK, "middle")
    b += text(826, 224, "&#8734;", 36, INK, "middle")
    save("card.svg", svg(W, 360, b, "Hey! I'm Deepanjali Vishwakarma. Homeland: Mumbai, Maharashtra, India. Class: Frontend developer. Special ability: Python, Linux, React and C++."))


# ---------- skills ----------
def skills():
    rows = [["HTML5", "CSS3", "JavaScript", "React"], ["Liquid", "Python", "C++"]]
    colors = [HOT, LAV, PEACH, BUB, PURPLE, HOT, LAV]
    tcols = [INK, INK, INK, INK, CREAM, INK, INK]
    rots = [-2.5, 2, -1.2, 2.6, 1.8, -2.2, 1.4]
    b, k, y = "", 0, 34
    for row in rows:
        widths = [len(s) * 17 + 52 for s in row]
        total = sum(widths) + 26 * (len(row) - 1)
        x = (W - total) / 2
        for s, w in zip(row, widths):
            b += box(x, y, w, 60, colors[k], sw=7, off=10, rot=rots[k])
            b += text(x + w / 2, y + 40, s, 26, tcols[k], "middle", tl=len(s) * 17)
            x += w + 26
            k += 1
        y += 90
    save("skills.svg", svg(W, 216, b, "Skills: HTML5, CSS3, JavaScript, React, Liquid, Python, C++"))


# ---------- section headings (alternate sides = asymmetry) ----------
def heading(name, s, fill, label, side):
    tl = len(s) * 19
    bw = tl + 84
    bx = 28 if side == "left" else W - 28 - 10 - bw
    b = box(bx, 28, bw, 62, fill, sw=SW, off=10, rot=-1 if side == "left" else 1)
    b += text(bx + bw / 2, 71, s, 30, INK, "middle", tl=tl)
    hx = bx + bw + 34 if side == "left" else bx - 34
    b += heart(hx, 60, 17, HOT, rot=10, sh=4, sw=5)
    save(name, svg(W, 120, b, label))


# ---------- buttons ----------
def button(name, s, fill, label):
    tl = max(len(s) * 21, 105)
    b = box(18, 20, 272, 78, fill, sw=SW, off=12)
    b += heart(58, 59, 13, CREAM, sh=0, sw=4, shadow=False)
    b += text(176, 70, s, 32, INK, "middle", tl=tl)
    save(name, svg(308, 124, b, label))


# ---------- footer ----------
def footer():
    b = box(22, 22, 868, 160, INK, sw=SW, off=18, shadow=HOT)
    b += text(W / 2, 98, "GURLY'S JOURNEY CONTINUES...", 38, PEACH, "middle", tl=740)
    b += text(W / 2, 156, "LEVEL UP NEVER ENDS!", 38, HOT, "middle", tl=540)
    b += heart(70, 70, 18, HOT, rot=-12, sh=0, sw=4, shadow=False)
    b += heart(854, 70, 18, HOT, rot=12, sh=0, sw=4, shadow=False)
    save("footer.svg", svg(W, 216, b, "Gurly's journey continues... level up never ends!"))


# ---------- profile picture frame ----------
def photo_b64(path):
    try:
        from PIL import Image, ImageOps
        im = Image.open(path).convert("RGB")
        im = ImageOps.fit(im, (484, 524))
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=85)
        return base64.b64encode(buf.getvalue()).decode(), "image/jpeg"
    except ImportError:
        mime = "image/png" if path.lower().endswith(".png") else "image/jpeg"
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode(), mime


def profile(photo=None):
    px, py, pw, ph = 44, 92, 242, 262
    b = window(20, 20, 290, 380, "marin.jpg", HOT, bg=PEACH)
    defs = ""
    if photo:
        data, mime = photo
        defs = f'<defs><clipPath id="ph"><rect x="{px}" y="{py}" width="{pw}" height="{ph}"/></clipPath></defs>'
        b += (f'<image xlink:href="data:{mime};base64,{data}" x="{px}" y="{py}" width="{pw}" height="{ph}" '
              f'preserveAspectRatio="xMidYMid slice" clip-path="url(#ph)"/>')
    else:
        defs = ('<defs><pattern id="hatch" width="16" height="16" patternUnits="userSpaceOnUse" '
                f'patternTransform="rotate(45)"><rect width="16" height="16" fill="{LAV}"/>'
                f'<rect width="6" height="16" fill="{CREAM}"/></pattern></defs>')
        b += f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="url(#hatch)"/>'
        b += box(px + 36, py + 100, 170, 46, CREAM, sw=6, off=6)
        b += text(px + 121, py + 130, "DROP PHOTO HERE", 15, INK, "middle", 700, MONO)
    b += f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="none" stroke="{INK}" stroke-width="{SW}"/>'
    b += text(165, 386, "MARIN.EXE", 26, INK, "middle", tl=200)
    b += heart(284, 340, 24, HOT, rot=12, sh=5, sw=6)
    b += sparkle(52, 98, 20, PURPLE, sh=4, sw=5)
    save("profile-picture.svg", svg(340, 432, b, "Marin Kitagawa", defs=defs))


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    cand = arg or os.path.join(ROOT, "marin.jpg")
    photo = photo_b64(cand) if os.path.exists(cand) else None
    if arg and not photo:
        sys.exit(f"photo not found: {arg}")
    marquee(); banner(); card(); skills()
    heading("h-snake.svg", "WATCH THE SNAKE EAT MY CONTRIBUTIONS", PEACH, "Watch the snake eat my contributions", "left")
    heading("h-connect.svg", "LET'S CONNECT", LAV, "Let's connect", "right")
    button("btn-email.svg", "EMAIL", HOT, "Email")
    button("btn-github.svg", "GITHUB", LAV, "GitHub")
    button("btn-instagram.svg", "INSTAGRAM", PEACH, "Instagram")
    footer()
    profile(photo)
    print("photo embedded" if photo else "placeholder frame (no photo found)", "->", OUT)


if __name__ == "__main__":
    main()
