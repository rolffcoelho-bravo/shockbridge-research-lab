from pathlib import Path
import math
import random
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3
from reportlab.lib import colors

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "reports" / "regime_question_research_desk.pdf"

W, H = A3  # portrait, one page


def hex_color(value):
    return colors.HexColor(value)


def draw_panel(c, x, y, w, h, stroke="#334155", fill="#0b1220", radius=14):
    c.setFillColor(hex_color(fill))
    c.setStrokeColor(hex_color(stroke))
    c.setLineWidth(0.8)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1)


def draw_title(c):
    c.setFillColor(hex_color("#fff7ed"))
    c.setFont("Times-Bold", 34)
    c.drawString(44, H - 66, "When Does a Market Shock Become a Regime Problem?")

    c.setFillColor(hex_color("#f5c76b"))
    c.setFont("Helvetica", 12)
    c.drawString(
        46,
        H - 88,
        "A public-safe institutional research-desk evidence map from isolated movement to regime-relevant transmission.",
    )

    c.setStrokeColor(hex_color("#d6a14a"))
    c.setLineWidth(0.6)
    c.line(44, H - 104, W - 44, H - 104)


def draw_answer_boxes(c):
    y = H - 220

    draw_panel(c, 44, y, 290, 92, stroke="#d6a14a", fill="#0b1220")
    c.setFillColor(hex_color("#f5c76b"))
    c.setFont("Helvetica-Bold", 7)
    c.drawString(62, y + 72, "ANSWER UPFRONT")

    c.setFillColor(colors.white)
    c.setFont("Times-Bold", 14)
    lines = [
        "A shock becomes regime-relevant when it",
        "spreads, persists, confirms across macro",
        "channels, and survives validation.",
    ]
    for i, line in enumerate(lines):
        c.drawString(62, y + 50 - i * 17, line)

    draw_panel(c, 352, y, W - 396, 92, stroke="#334155", fill="#111827")
    c.setFillColor(hex_color("#f5c76b"))
    c.setFont("Helvetica-Bold", 7)
    c.drawString(372, y + 72, "RESEARCH-DESK INTERPRETATION")

    c.setFillColor(hex_color("#cbd5e1"))
    c.setFont("Helvetica", 8.5)
    text = [
        "A large price move is not enough. The analytical question is whether the move remains isolated",
        "or becomes part of a broader transmission structure across rates, credit, FX, commodities,",
        "equities, volatility, and liquidity. This public artifact shows the logic without exposing",
        "private thresholds, weights, diagnostics, or action rules.",
    ]
    for i, line in enumerate(text):
        c.drawString(372, y + 52 - i * 13, line)


def draw_stage_boxes(c):
    y = H - 350
    x0 = 44
    gap = 10
    box_w = (W - 88 - 5 * gap) / 6
    box_h = 94

    stages = [
        ("1", "SHOCK ORIGIN", "A move begins in one asset, channel, geography, or narrative.", "#38bdf8"),
        ("2", "TRANSMISSION", "Stress spreads beyond the first market into correlated risk channels.", "#38bdf8"),
        ("3", "PERSISTENCE", "The signal survives beyond a temporary volatility spike.", "#f5c76b"),
        ("4", "CONFIRMATION", "Macro, curve, credit, FX, and commodities begin to align.", "#f5c76b"),
        ("5", "VALIDATION", "The pattern survives leakage control, alternative windows, and robustness checks.", "#fb7185"),
        ("6", "REGIME RISK", "The shock becomes structurally relevant instead of merely noisy.", "#ef4444"),
    ]

    for i, (n, title, desc, col) in enumerate(stages):
        x = x0 + i * (box_w + gap)
        draw_panel(c, x, y, box_w, box_h, stroke="#334155", fill="#0b1220", radius=10)

        c.setStrokeColor(hex_color(col))
        c.setFillColor(hex_color("#020617"))
        c.circle(x + 20, y + box_h - 22, 12, fill=1, stroke=1)

        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(x + 20, y + box_h - 25, n)

        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(x + 10, y + box_h - 46, title)

        c.setFillColor(hex_color("#cbd5e1"))
        c.setFont("Helvetica", 6.3)
        words = desc.split()
        line = ""
        lines = []
        for word in words:
            test = (line + " " + word).strip()
            if len(test) > 28:
                lines.append(line)
                line = word
            else:
                line = test
        if line:
            lines.append(line)

        for j, line in enumerate(lines[:4]):
            c.drawString(x + 10, y + box_h - 61 - j * 9, line)


def draw_evidence_stack(c):
    x, y, w, h = 44, 388, W - 88, 330
    draw_panel(c, x, y, w, h, stroke="#d6a14a", fill="#06101f", radius=16)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(x + w / 2, y + h - 34, "Transmission-to-Regime Evidence Stack")

    c.setFillColor(hex_color("#94a3b8"))
    c.setFont("Helvetica", 8)
    c.drawCentredString(
        x + w / 2,
        y + h - 50,
        "Conceptual public map. No private calibration, weights, thresholds, diagnostics, or action rules disclosed.",
    )

    # grid
    c.setStrokeColor(hex_color("#172033"))
    c.setLineWidth(0.4)
    for i in range(1, 12):
        gx = x + i * w / 12
        c.line(gx, y + 20, gx, y + h - 70)
    for j in range(1, 6):
        gy = y + 20 + j * (h - 90) / 6
        c.line(x + 14, gy, x + w - 14, gy)

    # heatmap
    hx, hy = x + 42, y + h - 135
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(hx, hy + 74, "Macro confirmation grid")
    heat_cols = ["#1d4ed8", "#2563eb", "#fbbf24", "#f97316", "#ef4444"]
    for r in range(4):
        for col_i in range(5):
            c.setFillColor(hex_color(heat_cols[min(4, max(0, col_i + (r % 2) - 1))]))
            c.rect(hx + col_i * 18, hy + r * 16, 16, 14, fill=1, stroke=0)

    # transmission curves
    random.seed(7)
    colors_list = ["#38bdf8", "#60a5fa", "#fbbf24", "#f97316", "#ef4444"]
    for k, col in enumerate(colors_list):
        c.setStrokeColor(hex_color(col))
        c.setLineWidth(1.2)
        path = c.beginPath()
        start_x = x + 100
        start_y = y + 90 + k * 16
        path.moveTo(start_x, start_y)
        for t in range(1, 9):
            px = x + 100 + t * 86
            py = y + 110 + 38 * math.sin(t * 0.95 + k * 0.75) + k * 10
            path.curveTo(px - 40, py + 30, px - 20, py - 30, px, py)
        c.drawPath(path, stroke=1, fill=0)

    # nodes
    for px, py, col in [
        (x + 100, y + 128, "#38bdf8"),
        (x + 315, y + 155, "#f5c76b"),
        (x + 560, y + 122, "#f97316"),
        (x + 760, y + 190, "#ef4444"),
        (x + 785, y + 235, "#ef4444"),
    ]:
        c.setFillColor(hex_color(col))
        c.circle(px, py, 4.5, fill=1, stroke=0)

    # out-of-sample discipline panel
    dx, dy = x + w - 260, y + h - 170
    draw_panel(c, dx, dy, 210, 82, stroke="#334155", fill="#111827", radius=8)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(dx + 12, dy + 62, "Out-of-sample discipline")
    c.setStrokeColor(hex_color("#38bdf8"))
    c.setLineWidth(1.1)
    pts = [(dx + 18, dy + 25), (dx + 45, dy + 38), (dx + 70, dy + 32), (dx + 95, dy + 48), (dx + 125, dy + 43), (dx + 160, dy + 55), (dx + 190, dy + 64)]
    for a, b in zip(pts, pts[1:]):
        c.line(a[0], a[1], b[0], b[1])
    c.setStrokeColor(hex_color("#f5c76b"))
    c.setDash(3, 3)
    c.line(dx + 110, dy + 18, dx + 110, dy + 68)
    c.setDash()

    # regime risk panel
    rx, ry = x + w - 260, y + 72
    draw_panel(c, rx, ry, 210, 100, stroke="#7f1d1d", fill="#190b0b", radius=10)
    c.setFillColor(hex_color("#fecaca"))
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(rx + 105, ry + 62, "REGIME RISK")
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(rx + 105, ry + 38, "ELEVATED")
    c.setFillColor(hex_color("#fecaca"))
    c.setFont("Helvetica", 7)
    c.drawCentredString(rx + 105, ry + 19, "only after evidence alignment")

    # continuum labels
    labels = [
        ("isolated move", "#93c5fd", x + 90),
        ("broadening stress", "#f5c76b", x + 295),
        ("validated transmission", "#f97316", x + 540),
        ("regime relevance", "#fecaca", x + 790),
    ]
    c.setFont("Helvetica", 7)
    for lab, col, lx in labels:
        c.setFillColor(hex_color(col))
        c.drawString(lx, y + 28, lab)


def draw_bottom_panels(c):
    y = 230
    panel_w = (W - 88 - 24) / 3

    panels = [
        ("EVIDENCE QUESTION", [("Is the move isolated?", "Start"), ("Is stress spreading?", "Transmission"), ("Does it persist?", "Regime pressure")]),
        ("DESK DISCIPLINE", [("Separate signal from story", "Required"), ("Control leakage risk", "Required"), ("Check stability", "Required")]),
        ("PUBLIC BOUNDARY", [("Thresholds", "Private"), ("Weights", "Private"), ("Action rules", "Private")]),
    ]

    for i, (title, rows) in enumerate(panels):
        x = 44 + i * (panel_w + 12)
        draw_panel(c, x, y, panel_w, 118, stroke="#334155", fill="#111827", radius=10)
        c.setFillColor(hex_color("#f5c76b"))
        c.setFont("Helvetica-Bold", 7)
        c.drawString(x + 14, y + 96, title)

        c.setFont("Helvetica", 8)
        for j, (left, right) in enumerate(rows):
            yy = y + 70 - j * 26
            c.setStrokeColor(hex_color("#334155"))
            c.line(x + 14, yy + 14, x + panel_w - 14, yy + 14)
            c.setFillColor(hex_color("#cbd5e1"))
            c.drawString(x + 14, yy, left)
            c.setFillColor(hex_color("#f5c76b"))
            c.setFont("Helvetica-Bold", 8)
            c.drawRightString(x + panel_w - 14, yy, right)
            c.setFont("Helvetica", 8)


def draw_bullets(c):
    x, y, w, h = 44, 74, W - 88, 132
    draw_panel(c, x, y, w, h, stroke="#d6a14a", fill="#0b1220", radius=12)

    c.setFillColor(hex_color("#f5c76b"))
    c.setFont("Times-Bold", 18)
    c.drawString(x + 18, y + h - 28, "Why this question matters")

    bullets = [
        "A large price move alone does not define a regime shift.",
        "A serious signal appears when stress transmits across markets rather than staying isolated.",
        "Persistence separates temporary volatility from structural pressure.",
        "Confirmation across macro and cross-asset channels increases decision relevance.",
        "Validation matters because robust signals must survive overfit, leakage, and narrative bias.",
    ]

    c.setFont("Helvetica", 9)
    c.setFillColor(colors.white)
    for i, b in enumerate(bullets):
        yy = y + h - 52 - i * 18
        c.setFillColor(hex_color("#f5c76b"))
        c.circle(x + 24, yy + 3, 5, fill=0, stroke=1)
        c.drawCentredString(x + 24, yy, str(i + 1))
        c.setFillColor(colors.white)
        c.drawString(x + 42, yy, b)


def build_research_desk_pdf() -> Path:
    PDF.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(PDF), pagesize=A3)

    # background
    c.setFillColor(hex_color("#05070d"))
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # subtle border
    c.setStrokeColor(hex_color("#d6a14a"))
    c.setLineWidth(0.8)
    c.rect(26, 26, W - 52, H - 52, fill=0, stroke=1)

    draw_title(c)
    draw_answer_boxes(c)
    draw_stage_boxes(c)
    draw_evidence_stack(c)
    draw_bottom_panels(c)
    draw_bullets(c)

    c.setFillColor(hex_color("#d6a14a"))
    c.setFont("Helvetica", 9)
    c.drawCentredString(
        W / 2,
        44,
        "Rodolfo Pereira · ShockBridge Research Lab · www.shockbridgepulse.com · rolffcoelho@hotmail.com · © 2026 Rodolfo P.",
    )

    c.showPage()
    c.save()
    return PDF


if __name__ == "__main__":
    output = build_research_desk_pdf()
    print(f"Generated research desk PDF: {output}")
