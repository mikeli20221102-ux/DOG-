# -*- coding: utf-8 -*-
"""Generate Pawsport English market research PDF with breed photos."""

import json
import urllib.request
from datetime import date
from pathlib import Path

from PIL import Image as PILImage
from PIL import ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable,
    Image as RLImage,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
IMG_DIR = Path(__file__).resolve().parent / "report-images"
OUT = ROOT / "Pawsport-Global-Market-Research-Report.pdf"

BREEDS = [
    {
        "key": "chow",
        "name": "Chow Chow",
        "rank": 1,
        "price_from": 1500,
        "range": "$1,500 – $4,500",
        "markets": "Middle East, Philippines, Russia",
        "demand": "92/100",
        "type": "Profit driver",
        "tagline": "Regal, iconic, premium status breed",
        "local": "chow-1.jpg",
        "remote": "https://dog.ceo/api/breed/chow/images/random",
        "accent": "#8B4513",
    },
    {
        "key": "shihtzu",
        "name": "Shih Tzu",
        "rank": 2,
        "price_from": 900,
        "range": "$900 – $2,700",
        "markets": "Korea, Japan, Southeast Asia",
        "demand": "88/100",
        "type": "Volume driver",
        "tagline": "Apartment-friendly, social-media friendly",
        "local": "shihtzu-1.jpg",
        "remote": "https://dog.ceo/api/breed/shihtzu/images/random",
        "accent": "#C4A484",
    },
    {
        "key": "crested",
        "name": "Chinese Crested",
        "rank": 3,
        "price_from": 1200,
        "range": "$1,200 – $3,600",
        "markets": "Korea, Japan, Middle East",
        "demand": "78/100",
        "type": "Balanced",
        "tagline": "Cabin-friendly, rare, low shedding",
        "local": "crested-1.jpg",
        "remote": None,
        "accent": "#E8B4B8",
    },
    {
        "key": "pekingese",
        "name": "Pekingese",
        "rank": 4,
        "price_from": 1000,
        "range": "$1,000 – $3,000",
        "markets": "Japan, Korea",
        "demand": "72/100",
        "type": "Moderate",
        "tagline": "Imperial lapdog, compact, Japan heritage",
        "local": "pekingese-1.jpg",
        "remote": "https://dog.ceo/api/breed/pug/images/random",
        "accent": "#D4A574",
    },
    {
        "key": "sharpei",
        "name": "Shar-Pei",
        "rank": 5,
        "price_from": 900,
        "range": "$900 – $2,700",
        "markets": "Middle East, Russia",
        "demand": "68/100",
        "type": "Profit driver",
        "tagline": "Distinctive wrinkles, loyal guardian",
        "local": "sharpei-1.jpg",
        "remote": "https://dog.ceo/api/breed/sharpei/images/random",
        "accent": "#A67B5B",
    },
    {
        "key": "chongqing",
        "name": "Chongqing Dog",
        "rank": 6,
        "price_from": 1800,
        "range": "$1,800 – $5,400",
        "markets": "Russia, collectors",
        "demand": "55/100",
        "type": "Collector niche",
        "tagline": "Extremely rare outside China",
        "local": "chongqing-1.jpg",
        "remote": None,
        "accent": "#5D4E37",
    },
]

HERO_LOCAL = "hero.jpg"


def _http_get(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": "PawsportReport/1.0"})
    return urllib.request.urlopen(req, timeout=timeout).read()


def _download_dog_ceo(api_url):
    payload = json.loads(_http_get(api_url))
    return _http_get(payload["message"])


def _font(size, bold=False):
    candidates = [
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\segoeui.ttf",
    ]
    for path in candidates:
        if Path(path).is_file():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _draw_dog_silhouette(draw, box, fill):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    draw.ellipse((cx - w * 0.22, y0 + h * 0.08, cx + w * 0.22, y0 + h * 0.38), fill=fill)
    draw.ellipse((x0 + w * 0.08, y0, x0 + w * 0.28, y0 + h * 0.18), fill=fill)
    draw.ellipse((x1 - w * 0.28, y0, x1 - w * 0.08, y0 + h * 0.18), fill=fill)
    draw.ellipse((cx - w * 0.34, cy - h * 0.02, cx + w * 0.34, y1 - h * 0.08), fill=fill)
    draw.ellipse((x0 + w * 0.12, y1 - h * 0.28, x0 + w * 0.28, y1 - h * 0.04), fill=fill)
    draw.ellipse((x1 - w * 0.28, y1 - h * 0.28, x1 - w * 0.12, y1 - h * 0.04), fill=fill)


def generate_breed_art(path, title, accent_hex, subtitle="Chinese native breed"):
    w, h = 800, 600
    accent = accent_hex.lstrip("#")
    r, g, b = int(accent[0:2], 16), int(accent[2:4], 16), int(accent[4:6], 16)
    img = PILImage.new("RGB", (w, h), (245, 247, 250))
    draw = ImageDraw.Draw(img)
    for i in range(h):
        t = i / h
        color = (
            int(245 + (r - 245) * t * 0.35),
            int(247 + (g - 247) * t * 0.35),
            int(250 + (b - 250) * t * 0.35),
        )
        draw.line([(0, i), (w, i)], fill=color)
    _draw_dog_silhouette(draw, (140, 80, 660, 460), (max(r - 40, 0), max(g - 40, 0), max(b - 40, 0)))
    draw.rounded_rectangle((0, h - 120, w, h), radius=0, fill=(26, 54, 93))
    draw.text((36, h - 92), title, fill="white", font=_font(42, bold=True))
    draw.text((36, h - 42), subtitle, fill=(200, 214, 229), font=_font(22))
    img.save(path, "JPEG", quality=90)


def save_resized_jpeg(src_bytes, dest, size=(800, 600)):
    from io import BytesIO

    img = PILImage.open(BytesIO(src_bytes)).convert("RGB")
    img.thumbnail(size, PILImage.Resampling.LANCZOS)
    canvas = PILImage.new("RGB", size, (245, 247, 250))
    ox = (size[0] - img.width) // 2
    oy = (size[1] - img.height) // 2
    canvas.paste(img, (ox, oy))
    canvas.save(dest, "JPEG", quality=90)


def build_hero_image(paths, dest):
    tiles = []
    for b in BREEDS[:6]:
        p = paths.get(f"{b['key']}.jpg")
        if p and Path(p).is_file():
            tiles.append(PILImage.open(p).convert("RGB"))
    if not tiles:
        generate_breed_art(dest, "Pawsport", "#2C5282", "Global puppy export")
        return dest
    tw, th = 900, 420
    tile_w = tw // 3
    tile_h = th // 2
    hero = PILImage.new("RGB", (tw, th), (26, 54, 93))
    for idx, tile in enumerate(tiles):
        row, col = divmod(idx, 3)
        t = tile.copy()
        t.thumbnail((tile_w - 4, tile_h - 4), PILImage.Resampling.LANCZOS)
        x = col * tile_w + (tile_w - t.width) // 2
        y = row * tile_h + (tile_h - t.height) // 2
        hero.paste(t, (x, y))
    hero.save(dest, "JPEG", quality=90)
    return dest


def ensure_images():
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    paths = {}

    for b in BREEDS:
        name = f"{b['key']}.jpg"
        cache = IMG_DIR / name
        local = ROOT / "assets" / "img" / b["local"]
        target = None

        if local.is_file() and local.stat().st_size > 5000:
            target = local
        elif cache.is_file() and cache.stat().st_size > 5000:
            target = cache
        else:
            try:
                if b["remote"]:
                    data = _download_dog_ceo(b["remote"])
                    save_resized_jpeg(data, cache)
                    target = cache
            except Exception:
                target = None
            if not target:
                subtitle = "Rare Chinese native breed" if b["key"] == "chongqing" else "Chinese native breed"
                generate_breed_art(cache, b["name"], b["accent"], subtitle)
                target = cache

        paths[name] = target

    hero_cache = IMG_DIR / "hero.jpg"
    build_hero_image(paths, hero_cache)
    paths["hero.jpg"] = hero_cache
    return paths


def scaled_image(path, max_w, max_h):
    if not path or not Path(path).is_file():
        return Spacer(max_w, max_h * 0.6)
    img = RLImage(str(path))
    iw, ih = img.imageWidth, img.imageHeight
    if not iw or not ih:
        return Spacer(max_w, max_h * 0.6)
    scale = min(max_w / iw, max_h / ih)
    img.drawWidth = iw * scale
    img.drawHeight = ih * scale
    img.hAlign = "CENTER"
    return img


def build_styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "title",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=30,
            alignment=TA_CENTER,
            spaceAfter=10,
            textColor=colors.HexColor("#1a365d"),
        ),
        "subtitle": ParagraphStyle(
            "subtitle",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=11,
            leading=15,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#4a5568"),
            spaceAfter=8,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            spaceBefore=12,
            spaceAfter=8,
            textColor=colors.HexColor("#2c5282"),
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=15,
            spaceBefore=8,
            spaceAfter=5,
            textColor=colors.HexColor("#2d3748"),
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            alignment=TA_LEFT,
            spaceAfter=5,
        ),
        "small": ParagraphStyle(
            "small",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=11,
            textColor=colors.HexColor("#718096"),
        ),
        "breed_name": ParagraphStyle(
            "breed_name",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            textColor=colors.HexColor("#1a365d"),
        ),
    }


def p(text, style):
    return Paragraph(text.replace("\n", "<br/>"), style)


def table(data, col_widths, header_rows=1, font_size=7.5):
    t = Table(data, colWidths=col_widths, repeatRows=header_rows)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, header_rows - 1), colors.HexColor("#2c5282")),
                ("TEXTCOLOR", (0, 0), (-1, header_rows - 1), colors.white),
                ("FONTNAME", (0, 0), (-1, header_rows - 1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), font_size),
                ("FONTNAME", (0, header_rows), (-1, -1), "Helvetica"),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e0")),
                ("ROWBACKGROUNDS", (0, header_rows), (-1, -1), [colors.white, colors.HexColor("#f7fafc")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return t


def breed_card(breed, img_path, styles):
    img = scaled_image(img_path, 4.2 * cm, 3.2 * cm)
    info = [
        p(f"#{breed['rank']} · {breed['name']}", styles["breed_name"]),
        Spacer(1, 4),
        p(f"<b>From:</b> ${breed['price_from']:,} &nbsp;|&nbsp; <b>Retail range:</b> {breed['range']}", styles["body"]),
        p(f"<b>Top markets:</b> {breed['markets']}", styles["body"]),
        p(f"<b>Demand index:</b> {breed['demand']} &nbsp;|&nbsp; <b>Role:</b> {breed['type']}", styles["body"]),
        p(f"<i>{breed['tagline']}</i>", styles["small"]),
    ]
    card = Table([[img, info]], colWidths=[4.5 * cm, 12.3 * cm])
    card.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f7fafc")),
                ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#cbd5e0")),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return card


def build_story(styles, images):
    s = styles
    today = date.today().isoformat()
    story = []
    page_w = A4[0] - 3 * cm

    # Cover
    hero = scaled_image(images.get("hero.jpg"), page_w, 7 * cm)
    story.append(Spacer(1, 0.4 * cm))
    story.append(hero)
    story.append(Spacer(1, 0.6 * cm))
    story.append(p("Pawsport Global Market Research Report", s["title"]))
    story.append(p("Chinese Native Breeds · Cross-Border B2C Export Analysis", s["subtitle"]))
    story.append(HRFlowable(width="75%", thickness=1, color=colors.HexColor("#2c5282"), hAlign="CENTER"))
    story.append(Spacer(1, 0.4 * cm))
    story.append(p(f"Report date: {today}", s["subtitle"]))
    story.append(p("Brand: Pawsport · silkroadpaws.com", s["subtitle"]))
    story.append(p("Markets: Korea, Japan, Middle East, Philippines, Southeast Asia, Russia", s["subtitle"]))
    story.append(Spacer(1, 0.5 * cm))

    thumb_row1, thumb_row2 = [], []
    for i, b in enumerate(BREEDS):
        cell = scaled_image(images.get(f"{b['key']}.jpg"), 2.6 * cm, 2 * cm)
        (thumb_row1 if i < 3 else thumb_row2).append(cell)
    thumbs = Table([thumb_row1, thumb_row2], colWidths=[5.6 * cm] * 3)
    thumbs.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    story.append(thumbs)
    story.append(PageBreak())

    # Executive summary
    story.append(p("1. Executive Summary", s["h1"]))
    story.append(
        p(
            "This report analyzes export opportunities for six Chinese native breeds across six target regions, "
            "covering <b>country fit</b>, <b>breed selection</b>, <b>retail pricing</b>, and <b>demand/volume outlook</b>. "
            "Official cross-border live-puppy sales data does not exist as a single public dataset; "
            "volume sections use <b>demand heat indices</b>, <b>volume ratings</b>, and <b>breed popularity benchmarks</b> instead.",
            s["body"],
        )
    )
    story.append(
        table(
            [
                ["Priority", "Market", "Key opportunity", "Demand", "Volume", "Margin"],
                ["P1", "South Korea", "Small breeds, fast entry after titer pass", "★★★★★", "High", "Med-High"],
                ["P1", "Philippines", "Chow premium + Shih Tzu volume; strong social", "★★★★☆", "High", "Med-High"],
                ["P1", "UAE / Saudi", "Rare imports, high ticket size", "★★★★☆", "Medium", "High"],
                ["P2", "Southeast Asia", "Shih Tzu volume; price-sensitive mid-tier", "★★★★☆", "High", "Medium"],
                ["P2", "Japan", "Shih Tzu / Pekingese heritage; 180-day wait", "★★★☆☆", "Medium", "High"],
                ["P3", "Russia", "Chow, Shar-Pei, Chongqing collector niche", "★★★☆☆", "Low-Med", "Med-High"],
            ],
            [1.2 * cm, 2.2 * cm, 5.8 * cm, 1.6 * cm, 1.4 * cm, 1.4 * cm],
        )
    )
    story.append(PageBreak())

    # Country markets
    story.append(p("2. Target Country Analysis", s["h1"]))
    story.append(
        table(
            [
                ["Market", "Buyer preference", "Lead breeds", "Local retail (USD)", "Export", "Demand", "Volume"],
                [
                    "South Korea",
                    "Tiny apartment dogs; Maltese/Poodle/Bichon dominate",
                    "Crested, Shih Tzu, Pekingese",
                    "$1,000–3,000",
                    "Easy",
                    "★★★★★",
                    "A — high volume",
                ],
                [
                    "Japan",
                    "Small breeds; Shih Tzu #13; Pekingese heritage",
                    "Shih Tzu, Pekingese, Crested",
                    "$1,000–4,000",
                    "Hard",
                    "★★★☆☆",
                    "B — moderate",
                ],
                [
                    "UAE / Saudi",
                    "Wealthy buyers; rare imports as status",
                    "Chow, Shar-Pei, Crested",
                    "$3,000–7,500",
                    "Medium",
                    "★★★★☆",
                    "B — moderate",
                ],
                [
                    "Philippines",
                    "Chow = premium icon; Shih Tzu hot",
                    "Chow, Shih Tzu, Pekingese",
                    "Chow $860–3,450",
                    "Medium",
                    "★★★★☆",
                    "A — high volume",
                ],
                [
                    "VN / TH / ID",
                    "Social commerce growth; mid + premium split",
                    "Shih Tzu, Pekingese, Chow",
                    "$400–1,500",
                    "Medium",
                    "★★★★☆",
                    "A — Shih Tzu volume",
                ],
                [
                    "Russia",
                    "Large / guard / rare collector breeds",
                    "Chow, Shar-Pei, Chongqing",
                    "$500–2,500",
                    "Medium",
                    "★★★☆☆",
                    "C — niche high value",
                ],
            ],
            [1.8 * cm, 3.2 * cm, 2.4 * cm, 2.2 * cm, 1.1 * cm, 1.3 * cm, 2.2 * cm],
            font_size=7,
        )
    )
    story.append(Spacer(1, 6))
    story.append(
        p(
            "Universal import baseline: ISO microchip + rabies vaccine + rabies titer (≥0.5 IU/mL) + health certificate + import permit.",
            s["small"],
        )
    )
    story.append(PageBreak())

    # Breed profiles with photos
    story.append(p("3. Breed Market Profiles (6 Chinese Breeds)", s["h1"]))
    story.append(
        p(
            "Listed by sales priority. List price on pawsport.netlify.app = base price up to 3× base (by coat quality, pedigree, delivery).",
            s["body"],
        )
    )
    story.append(Spacer(1, 8))
    for b in BREEDS:
        story.append(KeepTogether([breed_card(b, images.get(f"{b['key']}.jpg"), s), Spacer(1, 10)]))
    story.append(PageBreak())

    # Demand / volume
    story.append(p("4. Sales & Demand Outlook", s["h1"]))
    story.append(
        p(
            "No unified public database tracks commercial puppy exports by breed and country. "
            "The matrix below combines pet ownership trends, breed ranking data, import culture, and social-media demand signals.",
            s["body"],
        )
    )
    story.append(p("4.1 Breed × Country Demand Matrix", s["h2"]))
    matrix = [
        ["Breed \\ Market", "Korea", "Japan", "Middle East", "Philippines", "SEA", "Russia"],
        ["Chow Chow", "Med", "Low", "Very High", "Very High", "Med-High", "High"],
        ["Shih Tzu", "Very High", "High", "Med", "High", "Very High", "Med"],
        ["Chinese Crested", "High", "High", "Med-High", "Med", "Med", "Low"],
        ["Pekingese", "Med-High", "High", "Med", "Med", "Med", "Low"],
        ["Shar-Pei", "Low", "Low", "High", "Med", "Med", "High"],
        ["Chongqing Dog", "Low", "Low", "Med", "Low", "Low", "Med-High"],
    ]
    high_cells = [(1, 4), (1, 5), (2, 1), (2, 5), (3, 1), (3, 2), (4, 2), (5, 3), (5, 6), (6, 6)]
    t = Table(matrix, colWidths=[2.4 * cm, 1.7 * cm, 1.7 * cm, 1.9 * cm, 1.7 * cm, 1.7 * cm, 1.7 * cm], repeatRows=1)
    ms = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c5282")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e0")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7fafc")]),
    ]
    for r, c in high_cells:
        ms.append(("BACKGROUND", (c, r), (c, r), colors.HexColor("#c6f6d5")))
        ms.append(("FONTNAME", (c, r), (c, r), "Helvetica-Bold"))
    t.setStyle(TableStyle(ms))
    story.append(t)
    story.append(Spacer(1, 10))

    story.append(p("4.2 Monthly Pipeline Estimate (single kennel)", s["h2"]))
    story.append(
        table(
            [
                ["Scenario", "Inquiries/mo", "Closes/mo", "Lead breeds", "Lead markets", "Notes"],
                ["Conservative", "15–25", "2–4", "Shih Tzu, Crested", "Korea, Philippines", "Organic social only"],
                ["Baseline", "30–50", "5–8", "Shih Tzu, Chow", "KR + PH + SEA", "Daily Reels + weekly FB"],
                ["Aggressive", "60–100", "10–15", "Chow + Shih Tzu", "All targets", "Paid ads + KOL + fast WhatsApp"],
            ],
            [1.6 * cm, 1.8 * cm, 1.6 * cm, 2.6 * cm, 2.6 * cm, 4.6 * cm],
        )
    )
    story.append(Spacer(1, 6))
    story.append(
        p(
            "Assumed close rate 8–15% (long cycle, high consideration). Avg. ticket $1,200–3,500 incl. puppy, compliance, freight. "
            "Japan converts slower due to 180-day post-titer wait.",
            s["small"],
        )
    )
    story.append(PageBreak())

    # Price table
    story.append(p("5. Retail Price Comparison (USD)", s["h1"]))
    story.append(
        table(
            [
                ["Breed", "Pawsport from", "Korea", "Japan", "Middle East", "Philippines", "SEA", "Russia"],
                ["Chow Chow", "$1,500", "$2K–3.5K", "$2.5K–4K", "$3.5K–7.5K", "$860–3,450", "$800–2K", "$1.2K–2.5K"],
                ["Shih Tzu", "$900", "$1K–2.5K", "$1K–2.5K", "$1.5K–3K", "$520–1,720", "$400–1.2K", "$600–1.5K"],
                ["Chinese Crested", "$1,200", "$1.5K–3K", "$1.8K–3.5K", "$2.5K–5K", "$1K–2.5K", "$800–1.8K", "$1K–2K"],
                ["Pekingese", "$1,000", "$1.2K–2.8K", "$1.5K–3K", "$1.8K–3.5K", "$700–1.8K", "$500–1.2K", "$800–1.8K"],
                ["Shar-Pei", "$900", "$1.2K–2.5K", "$1.5K–3K", "$2K–4.5K", "$800–2K", "$600–1.5K", "$900–2.5K"],
                ["Chongqing Dog", "$1,800", "Rare", "Rare", "$3K–6K", "Rare", "Rare", "$1.8K–5.4K"],
            ],
            [2 * cm, 1.6 * cm, 1.6 * cm, 1.6 * cm, 1.8 * cm, 1.8 * cm, 1.4 * cm, 1.6 * cm],
            font_size=7,
        )
    )
    story.append(Spacer(1, 12))

    story.append(p("6. Strategic Recommendations", s["h1"]))
    for i, rec in enumerate(
        [
            "<b>Tier-1 markets:</b> Korea (Shih Tzu / Crested volume), Philippines (Chow margin + Shih Tzu volume), UAE (Chow / Shar-Pei premium).",
            "<b>Product mix:</b> Chow = status premium · Shih Tzu = apartment volume · Crested = cabin-friendly delivery · Chongqing = collector limited.",
            "<b>Pricing:</b> Base puppy price + destination freight quote; Middle East at upper range; competitive Shih Tzu in SEA.",
            "<b>Channel:</b> TikTok/Reels → silkroadpaws.com → WhatsApp / Facebook close (no online card checkout).",
            "<b>Compliance:</b> Chip + titer + health cert everywhere; disclose Japan 180-day wait; use IPATA shippers only — never crowd-courier platforms for live animals.",
        ],
        1,
    ):
        story.append(p(f"{i}. {rec}", s["body"]))
    story.append(Spacer(1, 10))

    story.append(p("7. Sources & Disclaimer", s["h1"]))
    for src in [
        "Korea small-dog trends — Korea JoongAng Daily (2025)",
        "Japan breed rankings — Anicom PR 2026 survey",
        "Middle East import pricing — PetsCaboodle",
        "Philippines retail prices — Digido Philippines",
        "Pawsport list prices — content/breeds.json (Jun 2026)",
        "Breed photos — dog.ceo API (open license) / project assets / branded artwork for rare breeds",
    ]:
        story.append(p(f"• {src}", s["small"]))
    story.append(Spacer(1, 6))
    story.append(
        p(
            "Disclaimer: Internal Pawsport reference only. Prices and regulations change. "
            "Volume figures are estimates, not official trade statistics. Verify destination import rules before each sale.",
            s["small"],
        )
    )
    return story


def main():
    images = ensure_images()
    styles = build_styles()
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=1.5 * cm,
        rightMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
        title="Pawsport Global Market Research Report",
        author="Pawsport",
    )

    def footer(canvas, doc_):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#718096"))
        canvas.drawString(1.5 * cm, 1 * cm, f"Pawsport Global Market Research · {date.today().isoformat()}")
        canvas.drawRightString(A4[0] - 1.5 * cm, 1 * cm, f"Page {doc_.page}")
        canvas.restoreState()

    doc.build(build_story(styles, images), onFirstPage=footer, onLaterPages=footer)
    print(f"Generated: {OUT}")
    for b in BREEDS:
        status = "OK" if images.get(f"{b['key']}.jpg") else "MISSING"
        print(f"  {b['name']}: {status}")


if __name__ == "__main__":
    main()
