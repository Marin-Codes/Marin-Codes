"""Builds the complete digital scrapbook page for Marin-Codes.
Composites all profile assets onto background2.jpg into assets/scrapbook-page.png and assets/scrapbook-page.svg.
"""
import os
import base64
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(ROOT, "assets")

def get_cropped(name):
    p = os.path.join(ASSETS, name)
    im = Image.open(p).convert("RGBA")
    b = im.getbbox()
    return im.crop(b) if b else im

def paste_img(dst, src, pos, size=None, rot=0):
    if size:
        src = src.resize(size, Image.LANCZOS)
    if rot != 0:
        src = src.rotate(rot, resample=Image.BICUBIC, expand=True)
    dst.alpha_composite(src, pos)

def main():
    bg_orig = Image.open(os.path.join(ASSETS, "background2.jpg")).convert("RGBA")
    scale = 2
    W, H = bg_orig.size[0] * scale, bg_orig.size[1] * scale
    canvas = bg_orig.resize((W, H), Image.LANCZOS)

    # Fonts
    font_title = ImageFont.truetype("C:/Windows/Fonts/courbd.ttf", 46)
    font_sub = ImageFont.truetype("C:/Windows/Fonts/segoeprb.ttf", 34)
    font_body = ImageFont.truetype("C:/Windows/Fonts/Inkfree.ttf", 36)
    font_note_h = ImageFont.truetype("C:/Windows/Fonts/comicbd.ttf", 40)
    font_note_b = ImageFont.truetype("C:/Windows/Fonts/Inkfree.ttf", 34)
    font_connect = ImageFont.truetype("C:/Windows/Fonts/segoeprb.ttf", 32)

    # 1. Title: about_me.png + bow + starburst
    about_me = get_cropped("about_me.png")
    # Content size is ~404x77, at 2x resize to ~740x140
    about_w, about_h = 740, int(740 * about_me.height / about_me.width)
    about_x = (W - about_w) // 2
    about_y = 190
    paste_img(canvas, about_me, (about_x, about_y), size=(about_w, about_h))

    # Bow on title (left)
    sticker11 = get_cropped("sticker11.png")
    paste_img(canvas, sticker11, (about_x - 70, about_y - 30), size=(130, 130), rot=-8)

    # Starburst on title (right)
    sticker7 = get_cropped("sticker7.png")
    paste_img(canvas, sticker7, (about_x + about_w - 50, about_y - 20), size=(120, 120), rot=12)

    # Pink rays accent
    sticker6 = get_cropped("sticker6.png")
    paste_img(canvas, sticker6, (140, 270), size=(90, 90), rot=-15)

    # 2. Newspaper Clipping: profile-section.png
    profile = get_cropped("profile-section.png")
    pw, ph = 730, int(730 * profile.height / profile.width)
    # Draw onto a transparent layer for the newspaper so we can tilt it
    np_layer = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    paste_img(np_layer, profile, (0, 0), size=(pw, ph))

    # Text inside the newspaper
    d_np = ImageDraw.Draw(np_layer)
    # The newsprint body starts around y=160 in the resized clipping
    text_x = 55
    curr_y = 175
    d_np.text((text_x, curr_y), "DEEPANJALI VISHWAKARMA", font=font_title, fill="#1c1924")
    curr_y += 58
    d_np.text((text_x, curr_y), "Frontend Developer · Code Artist", font=font_sub, fill="#7b2cbf")
    curr_y += 50
    d_np.text((text_x, curr_y), "📍 Mumbai, Maharashtra, India", font=font_body, fill="#3d3a45")
    curr_y += 52
    d_np.line([(text_x, curr_y), (pw - 60, curr_y)], fill="#d3c5b4", width=2)
    curr_y += 20
    d_np.text((text_x, curr_y), "♡ Cosplay my code, make it perfect!", font=font_body, fill="#2b2833")
    curr_y += 46
    d_np.text((text_x, curr_y), "♡ Turning coffee into code & code into art", font=font_body, fill="#2b2833")
    curr_y += 46
    d_np.text((text_x, curr_y), "♡ Making the web prettier, one pixel at a time", font=font_body, fill="#2b2833")
    curr_y += 46
    d_np.text((text_x, curr_y), "✦ Level: ∞   |   Special: Python, React & C++", font=font_body, fill="#e63946")

    # Paste rotated newspaper clipping onto canvas
    paste_img(canvas, np_layer, (70, 350), rot=-1.5)

    # Smart kitty sticker overlapping upper-right of newspaper
    smart_kitty = get_cropped("smart-kitty-sticker.png")
    paste_img(canvas, smart_kitty, (830, 360), size=(320, int(320 * smart_kitty.height / smart_kitty.width)), rot=4)

    # Paper hole & denim star on bottom edge of newspaper
    paper_hole = get_cropped("paper_hole.png")
    paste_img(canvas, paper_hole, (650, 830), size=(150, 150), rot=10)
    sticker4 = get_cropped("sticker4.png")
    paste_img(canvas, sticker4, (710, 870), size=(120, int(120 * sticker4.height / sticker4.width)), rot=14)

    # Cascading star trail along the right edge
    sticker2 = get_cropped("sticker2.png")
    paste_img(canvas, sticker2, (1170, 480), size=(110, int(110 * sticker2.height / sticker2.width)), rot=-2)

    # 3. Middle: Skills Sticky Note (Left) & Passions Blue Note (Right)
    # Left: Yellow pushpin note (scrap-note.png)
    scrap_note = get_cropped("scrap-note.png")
    sn_w, sn_h = 540, int(540 * scrap_note.height / scrap_note.width)
    sn_layer = Image.new("RGBA", (sn_w, sn_h), (0, 0, 0, 0))
    paste_img(sn_layer, scrap_note, (0, 0), size=(sn_w, sn_h))
    d_sn = ImageDraw.Draw(sn_layer)
    sn_tx = 75
    sn_ty = 130
    d_sn.text((sn_tx + 30, sn_ty), "✦ MY TOOLKIT ✦", font=font_note_h, fill="#9d0208")
    sn_ty += 62
    skills_list = [
        "• HTML5 & CSS3",
        "• JavaScript (ES6+)",
        "• React & Next.js",
        "• Python & C++",
        "• Linux & Bash",
        "• Git & GitHub",
        "• Liquid & Shopify",
        "• Figma & UI Design"
    ]
    for sk in skills_list:
        d_sn.text((sn_tx, sn_ty), sk, font=font_note_b, fill="#2b2b2b")
        sn_ty += 48

    paste_img(canvas, sn_layer, (90, 1020), rot=2.0)

    # Right: Blue crumpled paper with paperclip (note5.png)
    note5 = get_cropped("note5.png")
    n5_w, n5_h = 570, int(570 * note5.height / note5.width)
    n5_layer = Image.new("RGBA", (n5_w, n5_h), (0, 0, 0, 0))
    paste_img(n5_layer, note5, (0, 0), size=(n5_w, n5_h))
    d_n5 = ImageDraw.Draw(n5_layer)
    n5_tx = 70
    n5_ty = 110
    d_n5.text((n5_tx + 20, n5_ty), "✎ PASSIONS & GOALS", font=font_note_h, fill="#4361ee")
    n5_ty += 60
    goals = [
        "★ Crafting dreamy web UI",
        "★ Digital scrapbooks & art",
        "★ Open source contributions",
        "★ Creative algorithms & shaders",
        "★ Always learning, leveling up!",
        "Make it cute. Make it work. ♡"
    ]
    for g in goals:
        d_n5.text((n5_tx, n5_ty), g, font=font_note_b, fill="#1f2937")
        n5_ty += 48

    paste_img(canvas, n5_layer, (680, 1060), rot=-2.5)

    # Accents around middle notes
    # Vintage Camera with star flash
    sticker12 = get_cropped("sticker12.png")
    paste_img(canvas, sticker12, (680, 1590), size=(270, int(270 * sticker12.height / sticker12.width)), rot=3)

    # Pixel cursor arrow
    arrow = get_cropped("arrow.png")
    paste_img(canvas, arrow, (590, 1530), size=(85, int(85 * arrow.height / arrow.width)), rot=-15)

    # Yellow button star
    sticker8 = get_cropped("sticker8.png")
    paste_img(canvas, sticker8, (1100, 1540), size=(130, int(130 * sticker8.height / sticker8.width)), rot=10)

    # Stack of manuscript papers
    sticker3 = get_cropped("sticker3.png")
    paste_img(canvas, sticker3, (110, 1630), size=(140, int(140 * sticker3.height / sticker3.width)), rot=-5)

    # 4. Bottom: Music Discs (Left) + Vintage Phone & Connect Card (Right)
    # CD "The place where the confetto falls"
    disc2 = get_cropped("disc-sticker2.png")
    paste_img(canvas, disc2, (100, 1780), size=(320, int(320 * disc2.height / disc2.width)), rot=-6)

    # Vinyl record with stars overlapping CD
    disc1 = get_cropped("disc-sticker.png")
    paste_img(canvas, disc1, (300, 1830), size=(310, int(310 * disc1.height / disc1.width)), rot=14)

    # Vintage hanging telephone
    phone = get_cropped("let's-connect-sticker.png")
    paste_img(canvas, phone, (670, 1700), size=(85, int(85 * phone.height / phone.width)))

    # Cute Connect Card on the right of the phone
    card_w, card_h = 440, 290
    card_layer = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
    d_card = ImageDraw.Draw(card_layer)
    # Cream card with rounded corners and dotted border
    d_card.rounded_rectangle([(0, 0), (card_w - 1, card_h - 1)], radius=18, fill="#fffaf5", outline="#9d4edd", width=4)
    d_card.text((35, 25), "☎  LET'S CONNECT!", font=font_note_h, fill="#7209b7")
    d_card.line([(35, 75), (card_w - 35, 75)], fill="#ffb703", width=3)
    d_card.text((35, 95), "Instagram: @marin.codes", font=font_connect, fill="#3a0ca3")
    d_card.text((35, 145), "GitHub: @Marin-Codes", font=font_connect, fill="#3a0ca3")
    d_card.text((35, 195), "Pinterest: @Marin-Codes", font=font_connect, fill="#3a0ca3")
    d_card.text((35, 242), "Email: deepanjaliv567@gmail.com", font=ImageFont.truetype("C:/Windows/Fonts/segoeprb.ttf", 24), fill="#d90429")

    paste_img(canvas, card_layer, (780, 1760), rot=-1.5)

    # Ribbon paperclip pinned to the connect card
    sticker9 = get_cropped("sticker9.png")
    paste_img(canvas, sticker9, (750, 1720), size=(110, int(110 * sticker9.height / sticker9.width)), rot=-10)

    # Exclamation mark sticker beside connect card
    sticker5 = get_cropped("sticker5.png")
    paste_img(canvas, sticker5, (1200, 1780), size=(90, int(90 * sticker5.height / sticker5.width)), rot=12)

    # Output paths
    png_out = os.path.join(ASSETS, "scrapbook-page.png")
    canvas.save(png_out, "PNG", quality=95)
    print(f"Saved {png_out} ({os.path.getsize(png_out)} bytes)")

    # Also build SVG wrapper
    with open(png_out, "rb") as f:
        png_b64 = base64.b64encode(f.read()).decode("utf-8")

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="100%" height="auto" role="img" aria-label="Marin Codes Digital Scrapbook">
<title>Marin Codes Digital Scrapbook</title>
<image href="data:image/png;base64,{png_b64}" x="0" y="0" width="{W}" height="{H}"/>
</svg>'''
    svg_out = os.path.join(ASSETS, "scrapbook-page.svg")
    with open(svg_out, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Saved {svg_out} ({os.path.getsize(svg_out)} bytes)")

if __name__ == "__main__":
    main()
