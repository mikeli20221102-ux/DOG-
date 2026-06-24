# -*- coding: utf-8 -*-
"""Generate Pawsport global market research PDF report."""

from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Pawsport-全球市场调研报告.pdf"
FONT_REG = "MSYaHei"
FONT_BOLD = "MSYaHeiBold"


def register_fonts():
    pdfmetrics.registerFont(TTFont(FONT_REG, r"C:\Windows\Fonts\msyh.ttc", subfontIndex=0))
    pdfmetrics.registerFont(TTFont(FONT_BOLD, r"C:\Windows\Fonts\msyhbd.ttc", subfontIndex=0))


def build_styles():
    base = getSampleStyleSheet()
    styles = {
        "title": ParagraphStyle(
            "title",
            parent=base["Title"],
            fontName=FONT_BOLD,
            fontSize=22,
            leading=28,
            alignment=TA_CENTER,
            spaceAfter=12,
            textColor=colors.HexColor("#1a365d"),
        ),
        "subtitle": ParagraphStyle(
            "subtitle",
            parent=base["Normal"],
            fontName=FONT_REG,
            fontSize=11,
            leading=16,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#4a5568"),
            spaceAfter=24,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName=FONT_BOLD,
            fontSize=14,
            leading=20,
            spaceBefore=14,
            spaceAfter=8,
            textColor=colors.HexColor("#2c5282"),
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName=FONT_BOLD,
            fontSize=11,
            leading=16,
            spaceBefore=10,
            spaceAfter=6,
            textColor=colors.HexColor("#2d3748"),
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["Normal"],
            fontName=FONT_REG,
            fontSize=9,
            leading=14,
            alignment=TA_LEFT,
            spaceAfter=6,
        ),
        "small": ParagraphStyle(
            "small",
            parent=base["Normal"],
            fontName=FONT_REG,
            fontSize=8,
            leading=12,
            textColor=colors.HexColor("#718096"),
        ),
        "cell": ParagraphStyle(
            "cell",
            parent=base["Normal"],
            fontName=FONT_REG,
            fontSize=7.5,
            leading=10,
        ),
        "cell_bold": ParagraphStyle(
            "cell_bold",
            parent=base["Normal"],
            fontName=FONT_BOLD,
            fontSize=7.5,
            leading=10,
        ),
    }
    return styles


def p(text, style):
    return Paragraph(text.replace("\n", "<br/>"), style)


def table(data, col_widths, header_rows=1):
    t = Table(data, colWidths=col_widths, repeatRows=header_rows)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, header_rows - 1), colors.HexColor("#2c5282")),
        ("TEXTCOLOR", (0, 0), (-1, header_rows - 1), colors.white),
        ("FONTNAME", (0, 0), (-1, header_rows - 1), FONT_BOLD),
        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
        ("FONTNAME", (0, header_rows), (-1, -1), FONT_REG),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e0")),
        ("ROWBACKGROUNDS", (0, header_rows), (-1, -1), [colors.white, colors.HexColor("#f7fafc")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    t.setStyle(TableStyle(style_cmds))
    return t


def build_story(styles):
    today = date.today().isoformat()
    s = styles
    story = []

    # Cover
    story.append(Spacer(1, 3 * cm))
    story.append(p("Pawsport 全球宠物犬出口", s["title"]))
    story.append(p("市场调研报告", s["title"]))
    story.append(Spacer(1, 0.5 * cm))
    story.append(p("中国原生犬种 · 跨境 B2C · 目标市场分析", s["subtitle"]))
    story.append(HRFlowable(width="80%", thickness=1, color=colors.HexColor("#2c5282"), hAlign="CENTER"))
    story.append(Spacer(1, 0.8 * cm))
    story.append(p(f"报告日期：{today}", s["subtitle"]))
    story.append(p("适用品牌：Pawsport / silkroadpaws.com", s["subtitle"]))
    story.append(p("调研范围：韩国、日本、中东、菲律宾、东南亚、俄罗斯", s["subtitle"]))
    story.append(PageBreak())

    # Executive summary
    story.append(p("一、执行摘要", s["h1"]))
    story.append(
        p(
            "本报告基于公开行业数据、各国宠物消费趋势及 Pawsport 站点 6 个中国犬种的出口可行性分析，"
            "从<strong>目标国家</strong>、<strong>品种匹配</strong>、<strong>终端市场价格</strong>与"
            "<strong>需求/走量情况</strong>四个维度给出运营建议。"
            "需说明：跨境活体犬商业出口无统一官方销量统计，本报告「销量」以<strong>需求热度指数</strong>、"
            "<strong>走量评级</strong>及<strong>品种人气排名</strong>等可验证指标替代。",
            s["body"],
        )
    )
    summary_data = [
        ["优先级", "国家/地区", "核心机会", "需求热度", "走量潜力", "利润潜力"],
        ["P1", "韩国", "小型犬、公寓友好、滴度达标可快速入境", "★★★★★", "高", "中高"],
        ["P1", "菲律宾", "松狮高端爆款、社媒转化强", "★★★★☆", "高", "中高"],
        ["P1", "阿联酋/沙特", "稀有进口犬、高客单价", "★★★★☆", "中", "高"],
        ["P2", "东南亚(越泰印尼)", "西施走量、价格两极分化", "★★★★☆", "高", "中"],
        ["P2", "日本", "西施/京巴有渊源，但180天等待期", "★★★☆☆", "中", "高"],
        ["P3", "俄罗斯", "松狮/沙皮/重庆犬收藏向", "★★★☆☆", "中低", "中高"],
    ]
    story.append(table(summary_data, [1.2 * cm, 2.2 * cm, 5.5 * cm, 1.8 * cm, 1.5 * cm, 1.5 * cm]))
    story.append(Spacer(1, 8))

    story.append(p("二、目标国家市场分析", s["h1"]))
    country_data = [
        ["国家/地区", "市场偏好", "主推品种", "当地终端价(USD)", "出口难度", "需求热度", "走量评级", "备注"],
        [
            "韩国",
            "极爱小型犬，公寓文化，玛尔济斯/贵宾/比熊占主流",
            "冠毛犬、西施、京巴",
            "$1,000–3,000",
            "较易",
            "★★★★★",
            "A（高走量）",
            "滴度达标后入境快；可打「稀有中国血统」差异化",
        ],
        [
            "日本",
            "小型犬为主；西施人气第13；京巴(狆)有历史渊源",
            "西施、京巴、冠毛犬",
            "$1,000–4,000",
            "难",
            "★★★☆☆",
            "B（中等）",
            "采血后需等180天；周期长但客单价高",
        ],
        [
            "阿联酋/沙特",
            "高收入、爱稀有有面子的进口犬",
            "松狮、沙皮、冠毛犬",
            "$3,000–7,500(含运)",
            "中等",
            "★★★★☆",
            "B（中等）",
            "单票利润高；需进口许可与IPATA押运",
        ],
        [
            "菲律宾",
            "松狮为高端爆款；西施/博美热度高",
            "松狮、西施、京巴",
            "松狮$860–3,450\n西施$520–1,720",
            "中等",
            "★★★★☆",
            "A（高走量）",
            "Facebook/TikTok 转化强",
        ],
        [
            "越南/泰国/印尼",
            "社媒带货增长快，中端与高端两极",
            "西施、京巴、松狮",
            "$400–1,500",
            "中等",
            "★★★★☆",
            "A（西施走量）",
            "价格敏感，西施最适合走量",
        ],
        [
            "俄罗斯",
            "接受大型/护卫犬，稀有收藏向",
            "松狮、沙皮、重庆犬",
            "$500–2,500",
            "中等",
            "★★★☆☆",
            "C（小众高值）",
            "重庆犬可作收藏级高价",
        ],
    ]
    story.append(
        table(
            country_data,
            [1.6 * cm, 3.2 * cm, 2.4 * cm, 2.2 * cm, 1.2 * cm, 1.4 * cm, 1.6 * cm, 3.8 * cm],
        )
    )
    story.append(Spacer(1, 6))
    story.append(p("各国通用进口要求：ISO 芯片 + 狂犬疫苗 + 抗体滴度(≥0.5 IU/mL) + 健康证 + 进口许可", s["small"]))
    story.append(PageBreak())

    # Breed analysis
    story.append(p("三、品种市场分析（6 个中国犬种）", s["h1"]))
    breed_data = [
        ["排名", "品种", "英文名", "Pawsport起价", "挂牌区间(USD)", "最好卖国家", "需求指数", "走量/利润", "核心卖点"],
        ["1", "松狮", "Chow Chow", "$1,500", "$1,500–4,500", "中东、菲律宾、俄罗斯", "92/100", "利润型", "有面子、辨识度高、高端爆款"],
        ["2", "西施", "Shih Tzu", "$900", "$900–2,700", "韩国、日本、东南亚", "88/100", "走量型", "公寓友好、适应力强、社媒易传播"],
        ["3", "冠毛犬", "Chinese Crested", "$1,200", "$1,200–3,600", "韩国、日本、中东", "78/100", "均衡型", "可入客舱、稀有、低掉毛"],
        ["4", "京巴", "Pekingese", "$1,000", "$1,000–3,000", "日本、韩国", "72/100", "中等", "宫廷犬、小型、日本有渊源"],
        ["5", "沙皮", "Shar-Pei", "$900", "$900–2,700", "中东、俄罗斯", "68/100", "利润型", "褶皱辨识度高、护卫向"],
        ["6", "重庆犬", "Chongqing Dog", "$1,800", "$1,800–5,400", "俄罗斯、收藏家", "55/100", "收藏型", "极稀有、海外几乎见不到"],
    ]
    story.append(
        table(
            breed_data,
            [0.9 * cm, 1.2 * cm, 2.2 * cm, 1.6 * cm, 2.2 * cm, 2.8 * cm, 1.4 * cm, 1.4 * cm, 3.5 * cm],
        )
    )
    story.append(Spacer(1, 8))
    story.append(p("定价说明：挂牌价 = 起价 ～ 起价×3；上表为当地终端零售价参考，实际报价需叠加合规、运费与利润。", s["small"]))
    story.append(PageBreak())

    # Sales volume section
    story.append(p("四、销量与需求情况分析", s["h1"]))
    story.append(
        p(
            "跨境活体犬<strong>无各国统一公开销量数据库</strong>。以下结合各国养犬人口、品种人气榜、"
            "进口宠物消费趋势及社媒热度，给出<strong>需求热度指数</strong>与<strong>预估走量结构</strong>，"
            "供选品与投放参考。",
            s["body"],
        )
    )

    story.append(p("4.1 各国宠物市场背景（参考规模）", s["h2"]))
    market_size_data = [
        ["国家/地区", "养犬/宠物趋势", "小型犬占比倾向", "进口犬接受度", "对销量含义"],
        ["韩国", "都市化率高，宠物家庭化", "极高（公寓文化）", "高（愿为纯种付溢价）", "西施/冠毛询单量预期最高"],
        ["日本", "宠物市场成熟、监管严", "高", "中高（重血统品相）", "周期长，单笔转化价值高"],
        ["中东", "高净值人群多", "中（大型/稀有亦受欢迎）", "很高（进口=身份象征）", "松狮单票利润最大"],
        ["菲律宾", "社媒渗透率高、年轻宠主多", "高", "中高", "松狮+西施双引擎，转化快"],
        ["东南亚", "市场增速快", "高", "中（价格敏感）", "西施走量、松狮做利润款"],
        ["俄罗斯", "大型犬传统", "中低", "中", "重庆犬等稀有款小众高价"],
    ]
    story.append(table(market_size_data, [2 * cm, 3.5 * cm, 2.5 * cm, 2.5 * cm, 4.7 * cm]))
    story.append(Spacer(1, 10))

    story.append(p("4.2 品种×国家 需求/走量矩阵", s["h2"]))
    matrix_data = [
        ["品种 \\ 国家", "韩国", "日本", "中东", "菲律宾", "东南亚", "俄罗斯"],
        ["松狮", "中", "低", "极高", "极高", "中高", "高"],
        ["西施", "极高", "高", "中", "高", "极高", "中"],
        ["冠毛犬", "高", "高", "中高", "中", "中", "低"],
        ["京巴", "中高", "高", "中", "中", "中", "低"],
        ["沙皮", "低", "低", "高", "中", "中", "高"],
        ["重庆犬", "低", "低", "中", "低", "低", "中高"],
    ]
    high_cells = [
        (1, 4), (1, 5), (2, 1), (2, 5), (3, 1), (3, 2), (4, 2), (5, 3), (5, 6), (6, 6),
    ]
    t = Table(matrix_data, colWidths=[2.2 * cm, 1.8 * cm, 1.8 * cm, 1.8 * cm, 1.8 * cm, 1.8 * cm, 1.8 * cm], repeatRows=1)
    matrix_style = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c5282")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD),
        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
        ("FONTNAME", (0, 1), (-1, -1), FONT_REG),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e0")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7fafc")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    for r, c in high_cells:
        matrix_style.append(("BACKGROUND", (c, r), (c, r), colors.HexColor("#c6f6d5")))
        matrix_style.append(("FONTNAME", (c, r), (c, r), FONT_BOLD))
    t.setStyle(TableStyle(matrix_style))
    story.append(t)
    story.append(Spacer(1, 6))
    story.append(p("评级说明：极高=首选主推；高=重点投放；中=有机会；低=非优先", s["small"]))
    story.append(Spacer(1, 10))

    story.append(p("4.3 预估月度业务结构（单基地运营参考）", s["h2"]))
    forecast_data = [
        ["场景", "月询单(估)", "月成交(估)", "主力品种", "主力市场", "说明"],
        ["保守", "15–25", "2–4", "西施、冠毛", "韩国、菲律宾", "自然流量+社媒有机发帖"],
        ["基准", "30–50", "5–8", "西施、松狮", "韩+菲+东南亚", "TikTok/Reels 日更+FB 周帖"],
        ["积极", "60–100", "10–15", "松狮(利润)+西施(走量)", "全目标市场", "付费投流+KOL+WhatsApp 快速跟进"],
    ]
    story.append(table(forecast_data, [1.5 * cm, 1.8 * cm, 1.8 * cm, 2.5 * cm, 2.5 * cm, 5.1 * cm]))
    story.append(Spacer(1, 6))
    story.append(
        p(
            "注：成交率假设 8%–15%（活体高决策、长周期）；单票均价 $1,200–3,500（含犬价+合规+运费）。"
            "日本因180天等待，询单转化率通常低于韩国。",
            s["small"],
        )
    )
    story.append(PageBreak())

    # Price comparison
    story.append(p("五、市场价格对比总表", s["h1"]))
    price_data = [
        ["品种", "Pawsport起价", "韩国终端", "日本终端", "中东终端", "菲律宾终端", "东南亚终端", "俄罗斯终端"],
        ["松狮", "$1,500", "$2,000–3,500", "$2,500–4,000", "$3,500–7,500", "$860–3,450", "$800–2,000", "$1,200–2,500"],
        ["西施", "$900", "$1,000–2,500", "$1,000–2,500", "$1,500–3,000", "$520–1,720", "$400–1,200", "$600–1,500"],
        ["冠毛犬", "$1,200", "$1,500–3,000", "$1,800–3,500", "$2,500–5,000", "$1,000–2,500", "$800–1,800", "$1,000–2,000"],
        ["京巴", "$1,000", "$1,200–2,800", "$1,500–3,000", "$1,800–3,500", "$700–1,800", "$500–1,200", "$800–1,800"],
        ["沙皮", "$900", "$1,200–2,500", "$1,500–3,000", "$2,000–4,500", "$800–2,000", "$600–1,500", "$900–2,500"],
        ["重庆犬", "$1,800", "极少见", "极少见", "$3,000–6,000", "极少见", "极少见", "$1,800–5,400"],
    ]
    story.append(table(price_data, [1.6 * cm, 1.6 * cm, 1.8 * cm, 1.8 * cm, 1.8 * cm, 1.8 * cm, 1.8 * cm, 1.8 * cm]))
    story.append(Spacer(1, 10))

    story.append(p("六、战略建议", s["h1"]))
    recs = [
        "第一梯队市场：韩国（西施/冠毛走量）、菲律宾（松狮利润+西施走量）、阿联酋（松狮/沙皮高客单）。",
        "选品策略：松狮打「高端面子款」、西施打「走量公寓款」、冠毛打「客舱易交付款」、重庆犬打「收藏限量款」。",
        "定价策略：基础价 + 到岸运费分国报价；中东可挂区间上限；东南亚西施 Competitive 定价抢量。",
        "渠道策略：TikTok/Reels 短视频引流 → 独立站 silkroadpaws.com → WhatsApp/Facebook 成交。",
        "合规提醒：各国均需芯片+滴度+健康证；日本180天等待须提前告知；禁用 Grabr 等带货平台运活体。",
    ]
    for i, rec in enumerate(recs, 1):
        story.append(p(f"{i}. {rec}", s["body"]))
    story.append(Spacer(1, 12))

    story.append(p("七、数据来源与免责声明", s["h1"]))
    sources = [
        "韩国小型犬趋势：Korea JoongAng Daily (2025)",
        "日本犬种人气：Anicom PR 2026 犬种排行榜",
        "中东进口价参考：PetsCaboodle 定价研究",
        "菲律宾犬价：Digido Philippines 市场文章",
        "Pawsport 站点品种定价：content/breeds.json（2026-06）",
    ]
    for src in sources:
        story.append(p(f"• {src}", s["small"]))
    story.append(Spacer(1, 8))
    story.append(
        p(
            "免责声明：本报告仅供 Pawsport 内部运营参考。价格、法规及市场需求可能随时变化，"
            "「销量」为基于公开信息的估算与评级，非官方统计数据。成交前请核实目的国最新进口规定。",
            s["small"],
        )
    )

    return story


def main():
    register_fonts()
    styles = build_styles()
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=1.5 * cm,
        rightMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
        title="Pawsport 全球市场调研报告",
        author="Pawsport",
    )

    def footer(canvas, doc_):
        canvas.saveState()
        canvas.setFont(FONT_REG, 8)
        canvas.setFillColor(colors.HexColor("#718096"))
        canvas.drawString(1.5 * cm, 1 * cm, f"Pawsport 全球市场调研报告 · {date.today().isoformat()}")
        canvas.drawRightString(A4[0] - 1.5 * cm, 1 * cm, f"第 {doc_.page} 页")
        canvas.restoreState()

    doc.build(build_story(styles), onFirstPage=footer, onLaterPages=footer)
    print(f"Generated: {OUT}")


if __name__ == "__main__":
    main()
