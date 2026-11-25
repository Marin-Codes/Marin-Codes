"""Builds the complete digital scrapbook page for Marin-Codes.
Composites all profile assets onto background2.jpg into assets/scrapbook-page.png.
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(ROOT, "assets")

FONT_DIR = "C:/Windows/Fonts"


def get_cropped(name):
    p = os.path.join(ASSETS, name)
    im = Image.open(p).convert("RGBA")
    b = im.getbbox()
    return im.crop(b) if b else im


def add_soft_shadow(img, offset=(5, 7), radius=8, opacity=65):
    """Adds a subtle paper drop shadow behind a cutout PNG."""
    pad = radius * 2 + max(abs(offset[0]), abs(offset[1]))
    w, h = img.size
    shadow_canvas = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    alpha = img.getchannel("A").point(lambda a: int(a * opacity / 255))
    shadow = Image.new("RGBA", (w, h), (35, 15, 30, 255))
    shadow.putalpha(alpha)
    shadow_canvas.paste(shadow, (pad + offset[0], pad + offset[1]))
    shadow_canvas = shadow_canvas.filter(ImageFilter.GaussianBlur(radius))
    shadow_canvas.alpha_composite(img, (pad, pad))
    return shadow_canvas


def paste_img(dst, src, pos, size=None, rot=0, shadow=False):
    if size:
        src = src.resize(size, Image.LANCZOS)
    if shadow:
        src = add_soft_shadow(src)
    if rot != 0:
        src = src.rotate(rot, resample=Image.BICUBIC, expand=True)
    dst.alpha_composite(src, pos)


def draw_mixed_text(draw, pos, text, main_font, sym_font, fill, sym_fill=None):
    """Draws text using main_font for standard glyphs and sym_font for symbol icons, aligned on baseline."""
    x, y = pos
    sym_chars = set("♥★☆✿✦✎☎➤◈")
    sym_color = sym_fill or fill
    buf = ""
    is_sym_buf = None

    def flush(segment, is_sym, cur_x):
        if not segment:
            return cur_x
        f = sym_font if is_sym else main_font
        c = sym_color if is_sym else fill
        draw.text((cur_x, y), segment, font=f, fill=c, anchor="ls")
        return cur_x + f.getlength(segment)

    for ch in text:
        ch_is_sym = ch in sym_chars
        if is_sym_buf is None:
            is_sym_buf = ch_is_sym
            buf = ch
        elif ch_is_sym == is_sym_buf:
            buf += ch
        else:
            x = flush(buf, is_sym_buf, x)
            buf = ch
            is_sym_buf = ch_is_sym
    flush(buf, is_sym_buf, x)


def main():
    bg_orig = Image.open(os.path.join(ASSETS, "background2.jpg")).convert("RGBA")
    scale = 2
    W, H = bg_orig.size[0] * scale, bg_orig.size[1] * scale
    canvas = bg_orig.resize((W, H), Image.LANCZOS)

    # Fonts
    font_title = ImageFont.truetype(f"{FONT_DIR}/courbd.ttf", 38)
    font_sub = ImageFont.truetype(f"{FONT_DIR}/segoeprb.ttf", 29)
    font_body = ImageFont.truetype(f"{FONT_DIR}/segoepr.ttf", 26)
    font_body_bold = ImageFont.truetype(f"{FONT_DIR}/segoeprb.ttf", 25)
    font_sym_body = ImageFont.truetype(f"{FONT_DIR}/seguisym.ttf", 25)

    font_note_h = ImageFont.truetype(f"{FONT_DIR}/segoeprb.ttf", 33)
    font_sym_h = ImageFont.truetype(f"{FONT_DIR}/seguisym.ttf", 32)
    font_note_b = ImageFont.truetype(f"{FONT_DIR}/segoepr.ttf", 27)
    font_sym_note = ImageFont.truetype(f"{FONT_DIR}/seguisym.ttf", 26)

    font_connect_h = ImageFont.truetype(f"{FONT_DIR}/segoeprb.ttf", 31)
    font_connect = ImageFont.truetype(f"{FONT_DIR}/segoeprb.ttf", 25)
    font_connect_sm = ImageFont.truetype(f"{FONT_DIR}/segoeprb.ttf", 22)
    font_sym_conn = ImageFont.truetype(f"{FONT_DIR}/seguisym.ttf", 27)

    # ── 1. TOP TITLE: about_me.png + bow + starburst + rays ──────────
    about_me = get_cropped("about_me.png")
    about_w = 700
    about_h = int(about_w * about_me.height / about_me.width)
    about_x = (W - about_w) // 2
    about_y = 190
    paste_img(canvas, about_me, (about_x, about_y), size=(about_w, about_h))

    # Red gingham bow tucked cleanly to the top-left of 'A'
    sticker11 = get_cropped("sticker11.png")
    paste_img(canvas, sticker11, (about_x - 105, about_y - 45), size=(120, 120), rot=-10)

    # Pink spotlight rays to the right of 'ME'
    sticker7 = get_cropped("sticker7.png")
    paste_img(canvas, sticker7, (about_x + about_w + 5, about_y - 25), size=(110, 110), rot=14)

    # Pink gingham starburst accent lower-left
    sticker6 = get_cropped("sticker6.png")
    paste_img(canvas, sticker6, (105, 250), size=(95, 95), rot=-12)

    # ── 2. PROFILE NEWSPAPER CLIPPING + SMART KITTY ──────────────────
    profile = get_cropped("profile-section.png")
    pw = 735
    ph = int(pw * profile.height / profile.width)
    np_layer = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    paste_img(np_layer, profile, (0, 0), size=(pw, ph))

    d_np = ImageDraw.Draw(np_layer)
    tx = 72
    cy = 208
    draw_mixed_text(d_np, (tx, cy), "DEEPANJALI VISHWAKARMA", font_title, font_sym_body, "#1c1924")
    cy += 46
    draw_mixed_text(d_np, (tx, cy), "Frontend Developer · AI Developer", font_sub, font_sym_body, "#7b2cbf")
    cy += 40
    draw_mixed_text(d_np, (tx, cy), "♥ Mumbai, Maharashtra, India", font_body, font_sym_body, "#4a4752", sym_fill="#e0317a")
    cy += 18
    d_np.line([(tx, cy), (pw - 70, cy)], fill="#c8b8a6", width=2)
    cy += 38
    draw_mixed_text(d_np, (tx, cy), "♥ Cosplay my code, make it perfect!", font_body, font_sym_body, "#2b2833", sym_fill="#e0317a")
    cy += 39
    draw_mixed_text(d_np, (tx, cy), "♥ Turning coffee into code & code into art", font_body, font_sym_body, "#2b2833", sym_fill="#e0317a")
    cy += 39
    draw_mixed_text(d_np, (tx, cy), "♥ Making the web prettier, one pixel at a time", font_body, font_sym_body, "#2b2833", sym_fill="#e0317a")
    cy += 42
    draw_mixed_text(d_np, (tx, cy), "★ Level: ∞  |  Python, Linux, React & C++", font_body_bold, font_sym_body, "#c9184a", sym_fill="#f59f00")

    paste_img(canvas, np_layer, (66, 338), rot=-1.5, shadow=True)

    # Smart kitty overlapping upper-right area beside newspaper bio
    smart_kitty = get_cropped("smart-kitty-sticker.png")
    paste_img(canvas, smart_kitty, (855, 500), size=(320, int(320 * smart_kitty.height / smart_kitty.width)), rot=4)

    # Paper hole & denim star tucked cleanly at bottom-right edge below C++
    paper_hole = get_cropped("paper_hole.png")
    paste_img(canvas, paper_hole, (690, 865), size=(145, 145), rot=10)
    sticker4 = get_cropped("sticker4.png")
    paste_img(canvas, sticker4, (745, 895), size=(115, int(115 * sticker4.height / sticker4.width)), rot=14)

    # Cascading star trail along the right edge
    sticker2 = get_cropped("sticker2.png")
    paste_img(canvas, sticker2, (1170, 470), size=(110, int(110 * sticker2.height / sticker2.width)), rot=-2)

    # ── 3. MIDDLE: SKILLS (YELLOW NOTE) & PROJECTS (BLUE NOTE) ───────
    # Left: Yellow pushpin sticky note (note5.png)
    note5 = get_cropped("note5.png")
    n5_w = 565
    n5_h = int(n5_w * note5.height / note5.width)
    n5_layer = Image.new("RGBA", (n5_w, n5_h), (0, 0, 0, 0))
    paste_img(n5_layer, note5, (0, 0), size=(n5_w, n5_h))
    d_n5 = ImageDraw.Draw(n5_layer)
    n5_tx = 85
    n5_ty = 180  # Safely below the red pushpin, with generous bottom margin!
    draw_mixed_text(d_n5, (n5_tx + 28, n5_ty), "★ MY TOOLKIT ★", font_note_h, font_sym_h, "#9d0208", sym_fill="#e8590c")
    n5_ty += 48
    skills_list = [
        "• HTML5 & CSS3",
        "• JavaScript (ES6+)",
        "• React",
        "• Liquid",
        "• Python & C++",
        "• Linux, Git & GitHub",
        "• Figma & UI Design",
    ]
    for sk in skills_list:
        draw_mixed_text(d_n5, (n5_tx, n5_ty), sk, font_note_b, font_sym_note, "#1c1924")
        n5_ty += 42

    paste_img(canvas, n5_layer, (75, 1020), rot=2.0)

    # Right: Blue crumpled note with paperclip (scrap-note.png)
    scrap_note = get_cropped("scrap-note.png")
    sn_w = 580
    sn_h = int(sn_w * scrap_note.height / scrap_note.width)
    sn_layer = Image.new("RGBA", (sn_w, sn_h), (0, 0, 0, 0))
    paste_img(sn_layer, scrap_note, (0, 0), size=(sn_w, sn_h))
    d_sn = ImageDraw.Draw(sn_layer)
    sn_tx = 72
    sn_ty = 165
    draw_mixed_text(d_sn, (sn_tx + 10, sn_ty), "✎ PROJECTS & CODE", font_note_h, font_sym_h, "#3a0ca3", sym_fill="#7209b7")
    sn_ty += 52
    goals = [
        "★ Aesthetic web UI & CSS",
        "★ Digital scrapbooks & art",
        "★ Python automation tools",
        "★ Linux ricing & scripts",
        "★ Open source & shaders",
        "Make it cute. Make it work. ♥",
    ]
    for g in goals:
        draw_mixed_text(d_sn, (sn_tx, sn_ty), g, font_note_b, font_sym_note, "#1f2937", sym_fill="#e0317a")
        sn_ty += 47

    paste_img(canvas, sn_layer, (670, 1045), rot=-2.0)

    # Middle sticker accents
    sticker3 = get_cropped("sticker3.png")
    paste_img(canvas, sticker3, (95, 1615), size=(145, int(145 * sticker3.height / sticker3.width)), rot=-5)

    arrow = get_cropped("arrow.png")
    paste_img(canvas, arrow, (550, 1510), size=(85, int(85 * arrow.height / arrow.width)), rot=-15)

    sticker12 = get_cropped("sticker12.png")
    paste_img(canvas, sticker12, (645, 1540), size=(255, int(255 * sticker12.height / sticker12.width)), rot=3)

    sticker8 = get_cropped("sticker8.png")
    paste_img(canvas, sticker8, (1110, 1545), size=(125, int(125 * sticker8.height / sticker8.width)), rot=10)

    # ── 4. BOTTOM: MUSIC DISCS & TORN NOTEBOOK CONNECT CARD ──────────
    # CD "The place where the confetto falls"
    disc2 = get_cropped("disc-sticker2.png")
    paste_img(canvas, disc2, (95, 1855), size=(315, int(315 * disc2.height / disc2.width)), rot=-6)

    # Vinyl record with glitter stars overlapping CD
    disc1 = get_cropped("disc-sticker.png")
    paste_img(canvas, disc1, (295, 1840), size=(305, int(305 * disc1.height / disc1.width)), rot=14)

    # Vintage hanging telephone beside torn note
    phone = get_cropped("let's-connect-sticker.png")
    paste_img(canvas, phone, (625, 1690), size=(80, int(80 * phone.height / phone.width)))

    # Torn beige ruled notebook paper (note.png) as the Connect Card!
    note_page = get_cropped("note.png")
    np_w = 490
    np_h = int(np_w * note_page.height / note_page.width)  # ~397
    conn_layer = Image.new("RGBA", (np_w, np_h), (0, 0, 0, 0))
    paste_img(conn_layer, note_page, (0, 0), size=(np_w, np_h))
    d_conn = ImageDraw.Draw(conn_layer)

    # Text sits neatly to the right of the vertical margin line (~52px) aligned on ruled lines!
    cx = 68
    draw_mixed_text(d_conn, (cx, 94), "☎ LET'S CONNECT!", font_connect_h, font_sym_conn, "#7209b7", sym_fill="#e0317a")
    draw_mixed_text(d_conn, (cx, 155), "♥ IG: @deepu_yaps", font_connect, font_sym_conn, "#3a0ca3", sym_fill="#e0317a")
    draw_mixed_text(d_conn, (cx, 186), "♥ GH: @Marin-Codes", font_connect, font_sym_conn, "#3a0ca3", sym_fill="#e0317a")
    draw_mixed_text(d_conn, (cx, 217), "♥ deepanjaliv567@gmail.com", font_connect_sm, font_sym_conn, "#c9184a", sym_fill="#e0317a")
    draw_mixed_text(d_conn, (cx, 278), "✦ always down to collab! ✿", font_connect_sm, font_sym_conn, "#5c5346", sym_fill="#f59f00")

    paste_img(canvas, conn_layer, (720, 1745), rot=-1.5, shadow=True)

    # Pink ribbon paperclip clipped cleanly at the top edge of note.png
    sticker9 = get_cropped("sticker9.png")
    paste_img(canvas, sticker9, (795, 1685), size=(100, int(100 * sticker9.height / sticker9.width)), rot=-8)

    # Exclamation mark sticker above top-right corner of note.png
    sticker5 = get_cropped("sticker5.png")
    paste_img(canvas, sticker5, (1185, 1685), size=(85, int(85 * sticker5.height / sticker5.width)), rot=12)

    # Save optimized RGB PNG
    png_out = os.path.join(ASSETS, "scrapbook-page.png")
    canvas.convert("RGB").save(png_out, "PNG", optimize=True)
    print(f"Saved {png_out} ({os.path.getsize(png_out)} bytes)")

    # Remove oversized redundant SVG if present
    svg_old = os.path.join(ASSETS, "scrapbook-page.svg")
    if os.path.exists(svg_old):
        os.remove(svg_old)
        print(f"Removed redundant {svg_old}")


if __name__ == "__main__":
    main()
