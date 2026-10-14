"""Generate the README's pixel-art assets (light + dark) as crisp SVG.

Builds the banner, the footer, one thumbnail per featured project and the
section icons.

Usage: python pixelart.py [out_dir]   (defaults to this script's folder)
"""
import math
import random
import sys
from pathlib import Path

W, H = 320, 80

FONT = {
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "I": ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    ".": ["00000", "00000", "00000", "00100", "00000", "00000", "00000"],
    " ": ["00000"] * 7,
}

THEMES = {
    "dark": {
        "sky": ["#0b1021", "#0f1630", "#141d3f", "#1a254f", "#202d5e"],
        "star": "#e6edf3",
        "star_dim": "#7d8bb8",
        "orb": "#f2f0d8",
        "orb_shade": "#c9c6a8",
        "back": "#2a3868",
        "back_cap": "#5a6aa0",
        "front": "#151d3a",
        "front_cap": "#dfe6f5",
        "ground": "#0d1328",
        "text": "#f5f7ff",
        "shadow": "#4c5bd4",
        "tag": "#9fb0e0",
        "term_bg": "#0d1117",
        "term_border": "#3b4a7a",
        "term_bar": "#1f2a4d",
        "dots": ["#ff7b72", "#e3b341", "#7ee787"],
        "code": ["#79c0ff", "#d2a8ff", "#7ee787", "#ff7b72", "#e3b341"],
        "cursor": "#7ee787",
    },
    "light": {
        "sky": ["#a9d4ff", "#b8dcff", "#c8e4ff", "#d8ecff", "#e8f4ff"],
        "star": "#ffffff",
        "star_dim": "#ffffff",
        "orb": "#ffcf4a",
        "orb_shade": "#f5a524",
        "back": "#8fb8a0",
        "back_cap": "#c9ddd0",
        "front": "#4f7d61",
        "front_cap": "#ffffff",
        "ground": "#3e6450",
        "text": "#1b2540",
        "shadow": "#7ea6dd",
        "tag": "#2f4a78",
        "term_bg": "#ffffff",
        "term_border": "#8796b8",
        "term_bar": "#dde5f3",
        "dots": ["#cf222e", "#bf8700", "#1a7f37"],
        "code": ["#0969da", "#8250df", "#1a7f37", "#cf222e", "#9a6700"],
        "cursor": "#1a7f37",
    },
}


class Canvas:
    def __init__(self):
        self.parts = []

    def rect(self, x, y, w, h, fill, cls=None):
        c = f' class="{cls}"' if cls else ""
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"{c}/>')

    def text(self, s, x, y, scale, fill, spacing=1):
        """Draw text with the 5x7 font, merging horizontal runs into one rect."""
        cx = x
        for ch in s:
            glyph = FONT[ch]
            for row, bits in enumerate(glyph):
                col = 0
                while col < 5:
                    if bits[col] == "1":
                        start = col
                        while col < 5 and bits[col] == "1":
                            col += 1
                        self.rect(cx + start * scale, y + row * scale,
                                  (col - start) * scale, scale, fill)
                    else:
                        col += 1
            cx += (5 + spacing) * scale
        return cx


def text_width(s, scale, spacing=1):
    return len(s) * (5 + spacing) * scale - spacing * scale


def ridge(seed, base, amp, peaks):
    """Height (in px from top) per column for a stepped mountain ridge."""
    rnd = random.Random(seed)
    centers = [(rnd.uniform(0, W), rnd.uniform(0.5, 1.0) * amp, rnd.uniform(18, 40)) for _ in range(peaks)]
    out = []
    for x in range(W):
        h = 0.0
        for cx, a, wdt in centers:
            h = max(h, a * max(0.0, 1 - abs(x - cx) / wdt))
        out.append(int(base - h))
    # quantize into 2px steps for a chunkier pixel look
    return [v - (v % 2) for v in out]


def build_banner(theme_name):
    t = THEMES[theme_name]
    c = Canvas()

    # Sky: banded gradient with a dithered seam between bands.
    band_h = 12
    for i, col in enumerate(t["sky"]):
        c.rect(0, i * band_h, W, band_h if i < len(t["sky"]) - 1 else H - i * band_h, col)
        if i > 0:
            prev = t["sky"][i - 1]
            for x in range(0, W, 2):
                c.rect(x + (i % 2), i * band_h, 1, 1, prev)

    rnd = random.Random(7)
    if theme_name == "dark":
        for _ in range(55):
            x, y = rnd.randrange(W), rnd.randrange(0, 40)
            c.rect(x, y, 1, 1, t["star"] if rnd.random() > 0.5 else t["star_dim"])
        for i, (x, y) in enumerate([(150, 8), (205, 22), (118, 32), (300, 6)]):
            cls = "tw" if i % 2 == 0 else "tw2"
            c.rect(x, y - 1, 1, 3, t["star"], cls)
            c.rect(x - 1, y, 3, 1, t["star"], cls)
    else:
        # Pixel clouds.
        for cx, cy in [(132, 10), (196, 26), (20, 50)]:
            c.rect(cx, cy, 14, 2, t["star"])
            c.rect(cx + 3, cy - 2, 7, 2, t["star"])
            c.rect(cx - 2, cy + 2, 18, 2, t["star"])

    # Moon or sun: a stepped pixel disc.
    ox, oy, r = 178, 12, 6
    for dy in range(-r, r + 1):
        half = int(math.sqrt(max(0, r * r - dy * dy)) + 0.5)
        c.rect(ox - half, oy + dy, 2 * half, 1, t["orb"])
    if theme_name == "dark":
        c.rect(ox - 2, oy - 2, 2, 2, t["orb_shade"])
        c.rect(ox + 1, oy + 2, 3, 2, t["orb_shade"])
    else:
        for dx, dy in [(-10, 0), (9, 0), (0, -10), (0, 9), (-7, -7), (6, -7), (-7, 6), (6, 6)]:
            c.rect(ox + dx, oy + dy, 2, 2, t["orb_shade"])

    # Two mountain ranges (the Andes, loosely) with caps on the tallest peaks.
    for seed, base, amp, peaks, body, cap, cap_line in [
        (3, 70, 34, 9, t["back"], t["back_cap"], 44),
        (11, 80, 26, 11, t["front"], t["front_cap"], 0),
    ]:
        heights = ridge(seed, base, amp, peaks)
        x = 0
        while x < W:
            h = heights[x]
            start = x
            while x < W and heights[x] == h:
                x += 1
            c.rect(start, h, x - start, H - h, body)
            if h < cap_line:
                c.rect(start, h, x - start, min(2, cap_line - h), cap)
    c.rect(0, 76, W, 4, t["ground"])

    # Name with a 1px drop shadow, then the tagline.
    name, scale = "KEVELMUN", 3
    nx, ny = 22, 14
    c.text(name, nx + 1, ny + 2, scale, t["shadow"])
    c.text(name, nx, ny, scale, t["text"])
    c.text("BUILD . SHIP . LEAD", nx, ny + 7 * scale + 8, 1, t["tag"], spacing=2)

    # Small code terminal.
    tx, ty, tw, th = 232, 12, 68, 40
    c.rect(tx - 1, ty - 1, tw + 2, th + 2, t["term_border"])
    c.rect(tx, ty, tw, th, t["term_bg"])
    c.rect(tx, ty, tw, 6, t["term_bar"])
    for i, dot in enumerate(t["dots"]):
        c.rect(tx + 3 + i * 4, ty + 2, 2, 2, dot)
    code_lines = [
        [(0, 8, 0), (10, 14, 1)],
        [(4, 10, 2), (16, 6, 3)],
        [(4, 18, 1), (24, 8, 4)],
        [(8, 12, 0), (22, 10, 2)],
        [(0, 6, 3)],
    ]
    for i, segs in enumerate(code_lines):
        for off, ln, ci in segs:
            c.rect(tx + 4 + off, ty + 10 + i * 5, ln, 2, t["code"][ci])
    py = ty + 10 + len(code_lines) * 5
    c.rect(tx + 4, py, 2, 2, t["cursor"])
    c.rect(tx + 8, py - 1, 3, 4, t["cursor"], "cur")

    label = (
        "Pixel art banner with the name kevelmun and the words build, ship, lead, "
        "over mountains and a small code terminal"
    )
    style = (
        "<style>"
        "@keyframes blink{50%{opacity:0}}"
        "@keyframes twinkle{50%{opacity:.25}}"
        ".cur{animation:blink 1.1s steps(1) infinite}"
        ".tw{animation:twinkle 2.4s steps(2) infinite}"
        ".tw2{animation:twinkle 3.1s steps(2) infinite .8s}"
        "@media (prefers-reduced-motion:reduce){.cur,.tw,.tw2{animation:none}}"
        "</style>"
    )
    return svg(c, W, H, 4, label, style)


def svg(c, w, h, scale, label, style=""):
    a11y = f'role="img" aria-label="{label}"><title>{label}</title>' if label else 'aria-hidden="true">'
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w * scale}" height="{h * scale}" shape-rendering="crispEdges" '
        + a11y + style + "".join(c.parts) + "</svg>\n"
    )


# --- Footer ---------------------------------------------------------------

def build_footer(theme_name):
    """The banner's mountains, on a transparent sky, to close the page."""
    t = THEMES[theme_name]
    c = Canvas()
    fh = 24
    for seed, base, amp, peaks, body in [
        (3, 20, 14, 9, t["back"]),
        (11, 24, 10, 11, t["front"]),
    ]:
        heights = ridge(seed, base, amp, peaks)
        x = 0
        while x < W:
            h = heights[x]
            start = x
            while x < W and heights[x] == h:
                x += 1
            c.rect(start, h, x - start, fh - h, body)
    c.rect(0, fh - 2, W, 2, t["ground"])
    return svg(c, W, fh, 4, "")


# --- Project thumbnails ---------------------------------------------------

TW, TH = 96, 48

# Colors that live on a screen stay the same in both themes.
SCREEN = {
    "bg": "#0d1117", "gutter": "#161b22", "text": "#c9d1d9",
    "green": "#7ee787", "blue": "#79c0ff", "purple": "#d2a8ff",
    "red": "#ff7b72", "amber": "#e3b341",
}

THUMB = {
    "dark": {
        "bg": "#141d3f", "dot": "#26315c", "outline": "#05081a",
        "paper": "#dfe6f5", "grey": "#8b98b8", "grey_d": "#4a5680",
        "green": "#3fb950", "blue": "#58a6ff", "purple": "#a371f7",
        "red": "#f85149", "amber": "#e3b341", "orange": "#d18616",
        "leaf": "#3fb950", "leaf_d": "#238636", "line": "#5a6aa0",
    },
    "light": {
        "bg": "#e3f0ff", "dot": "#c8def7", "outline": "#1b2540",
        "paper": "#ffffff", "grey": "#9aa8c7", "grey_d": "#5b6b8f",
        "green": "#2da44e", "blue": "#0969da", "purple": "#8250df",
        "red": "#cf222e", "amber": "#e3b341", "orange": "#bc4c00",
        "leaf": "#2da44e", "leaf_d": "#1a7f37", "line": "#7e8db0",
    },
}


def frame(c, x, y, w, h, fill, outline):
    """Filled box with a 1px outline and clipped corners."""
    c.rect(x + 1, y, w - 2, 1, outline)
    c.rect(x + 1, y + h - 1, w - 2, 1, outline)
    c.rect(x, y + 1, 1, h - 2, outline)
    c.rect(x + w - 1, y + 1, 1, h - 2, outline)
    c.rect(x + 1, y + 1, w - 2, h - 2, fill)


def dashes(c, x0, x1, y, color):
    for x in range(x0, x1, 3):
        c.rect(x, y, 2, 1, color)


def thumb_background(c, p):
    c.rect(0, 0, TW, TH, p["bg"])
    rnd = random.Random(5)
    for _ in range(26):
        c.rect(rnd.randrange(TW), rnd.randrange(TH), 1, 1, p["dot"])


def check(c, x, y, color):
    """A 2px-thick check mark whose short arm starts at (x, y)."""
    for i in range(3):
        c.rect(x + i, y + i, 2, 2, color)
    for i in range(6):
        c.rect(x + 3 + i, y + 1 - i, 2, 2, color)


def thumb_sotita(c, p):
    # Phone with a finance dashboard.
    frame(c, 12, 4, 22, 40, p["grey"], p["outline"])
    c.rect(14, 7, 18, 31, SCREEN["bg"])
    c.rect(20, 5, 6, 1, p["outline"])
    c.rect(21, 40, 4, 2, p["outline"])
    c.rect(16, 9, 6, 1, SCREEN["text"])
    c.rect(16, 11, 11, 2, SCREEN["green"])
    for x, h, col in [(16, 4, "green"), (19, 7, "blue"), (22, 5, "purple"), (25, 9, "blue"), (28, 6, "amber")]:
        c.rect(x, 26 - h, 2, h, SCREEN[col])
    for y, col in [(29, "red"), (32, "green"), (35, "red")]:
        c.rect(16, y, 5, 1, SCREEN[col])
        c.rect(24, y, 6, 1, SCREEN["text"])
    # Coin stacks.
    for x, ys in [(42, (35, 32, 29, 26)), (56, (35, 32))]:
        for y in ys:
            frame(c, x, y, 12, 5, p["amber"], p["outline"])
            c.rect(x + 1, y + 3, 10, 1, p["orange"])
    # Cloud with sync arrows, linked to the phone by a dashed line.
    frame(c, 64, 12, 22, 10, p["paper"], p["outline"])
    frame(c, 68, 7, 12, 7, p["paper"], p["outline"])
    c.rect(69, 12, 10, 2, p["paper"])
    c.rect(69, 15, 8, 1, p["blue"])
    c.rect(76, 14, 1, 3, p["blue"])
    c.rect(72, 18, 8, 1, p["blue"])
    c.rect(72, 17, 1, 3, p["blue"])
    dashes(c, 36, 63, 17, p["line"])


def thumb_cv(c, p):
    # CV page with a folded corner and highlighted keywords.
    frame(c, 12, 4, 28, 40, p["paper"], p["outline"])
    for i in range(6):
        c.rect(34 + i, 4 + i, 6 - i, 1, p["bg"])
        c.rect(34 + i, 4 + i, 1, 1, p["outline"])
    c.rect(34, 5, 1, 5, p["outline"])
    c.rect(34, 10, 6, 1, p["outline"])
    c.rect(35, 6, 4, 4, p["grey"])
    c.rect(16, 8, 12, 2, p["blue"])
    c.rect(16, 11, 8, 1, p["grey"])
    for y in (15, 24, 33):
        c.rect(16, y, 7, 1, p["blue"])
        for k in range(1, 4):
            if y + 2 * k < 42:
                c.rect(16, y + 2 * k, 20 - 3 * (k % 2), 1, p["grey"])
    c.rect(20, 17, 7, 1, p["amber"])
    c.rect(24, 26, 8, 1, p["amber"])
    c.rect(18, 37, 6, 1, p["amber"])
    # AI sparkles.
    c.rect(51, 6, 1, 7, p["purple"])
    c.rect(48, 9, 7, 1, p["purple"])
    c.rect(58, 14, 1, 3, p["purple"])
    c.rect(57, 15, 3, 1, p["purple"])
    # Verified badge and the two output files.
    dashes(c, 42, 54, 31, p["line"])
    frame(c, 55, 23, 18, 17, p["green"], p["outline"])
    check(c, 58, 30, p["paper"])
    for y, col in [(24, "blue"), (33, "red")]:
        frame(c, 78, y, 12, 7, p[col], p["outline"])
        c.rect(80, y + 3, 8, 1, p["paper"])


def thumb_spring(c, p):
    # Editor with a gutter of pass/fail markers and a lint squiggle.
    frame(c, 6, 4, 58, 40, SCREEN["bg"], p["outline"])
    c.rect(7, 5, 56, 4, p["grey_d"])
    for i, col in enumerate(("red", "amber", "green")):
        c.rect(9 + 3 * i, 6, 2, 2, SCREEN[col])
    c.rect(7, 9, 5, 34, SCREEN["gutter"])
    lines = [
        [(0, 6, "purple"), (8, 12, "blue")],
        [(3, 8, "blue"), (13, 10, "text")],
        [(3, 5, "purple"), (10, 14, "amber")],
        [(6, 16, "text"), (24, 6, "green")],
        [(6, 10, "blue"), (18, 12, "text")],
        [(3, 12, "text")],
        [(0, 2, "purple")],
    ]
    for i, segs in enumerate(lines):
        y = 12 + 4 * i
        c.rect(9, y, 2, 2, SCREEN["red"] if i == 3 else SCREEN["green"])
        for off, ln, col in segs:
            c.rect(14 + off, y, ln, 2, SCREEN[col])
    for x in range(20, 36, 2):
        c.rect(x, 26 + (x // 2) % 2, 1, 1, SCREEN["red"])
    # Spring-style leaf with a check badge.
    cx, cy, a, b = 78, 19, 13, 6.5
    for y in range(cy - 12, cy + 13):
        row = []
        for x in range(cx - 12, cx + 13):
            # Rotate 45 degrees so the leaf points to the upper right.
            u = ((x - cx) - (y - cy)) / math.sqrt(2)
            v = ((x - cx) + (y - cy)) / math.sqrt(2)
            if abs(u) <= a and abs(v) <= b * (1 - (u / a) ** 2):
                row.append(p["leaf_d"] if abs(v) < 0.75 and u > -a + 3 else p["leaf"])
            else:
                row.append(None)
        x = 0
        while x < len(row):
            start = x
            while x < len(row) and row[x] == row[start]:
                x += 1
            if row[start]:
                c.rect(cx - 12 + start, y, x - start, 1, row[start])
    for i in range(4):
        c.rect(cx - 10 - i, cy + 10 + i, 2, 1, p["leaf_d"])
    frame(c, 80, 30, 13, 13, p["paper"], p["outline"])
    check(c, 82, 35, p["green"])


HEAT = ["#0d1b4c", "#252a8a", "#5a2ea6", "#a3317a", "#de4b3e", "#f39a2b", "#ffe066"]


def thumb_stereo(c, p):
    # Stereo rig (two cameras) above a thermal camera.
    c.rect(8, 15, 38, 3, p["grey_d"])
    for x in (8, 32):
        frame(c, x, 7, 14, 10, p["grey"], p["outline"])
        frame(c, x + 3, 9, 8, 7, SCREEN["bg"], p["outline"])
        c.rect(x + 5, 11, 4, 3, p["blue"])
    frame(c, 20, 24, 14, 10, p["orange"], p["outline"])
    frame(c, 23, 26, 8, 7, SCREEN["bg"], p["outline"])
    c.rect(25, 28, 4, 3, p["red"])
    c.rect(26, 34, 2, 8, p["grey_d"])
    c.rect(20, 42, 14, 2, p["grey_d"])
    dashes(c, 37, 51, 29, p["line"])
    # Thermal image of a person, drawn in 2x2 blocks.
    px, py, pw, ph = 52, 6, 38, 36
    frame(c, px, py, pw, ph, HEAT[0], p["outline"])
    for by in range(py + 1, py + ph - 1, 2):
        for bx in range(px + 1, px + pw - 1, 2):
            head = math.exp(-(((bx - 71) / 5) ** 2 + ((by - 15) / 5) ** 2))
            body = math.exp(-(((bx - 71) / 9) ** 2 + ((by - 33) / 9) ** 2))
            v = max(head, body * 0.9)
            idx = min(len(HEAT) - 1, int(v * len(HEAT)))
            if idx:
                c.rect(bx, by, 2, 2, HEAT[idx])


THUMBS = {
    "sotita": (thumb_sotita, "Pixel art: a phone with a finance dashboard, coins and a cloud syncing"),
    "cv-adapter": (thumb_cv, "Pixel art: a CV page with highlighted keywords, AI sparkles and a check badge"),
    "spring-validator": (thumb_spring, "Pixel art: a code editor with lint markers next to a green leaf"),
    "stereothermal": (thumb_stereo, "Pixel art: two stereo cameras and a thermal camera next to a heat map"),
}


def build_thumb(key, theme_name):
    draw, label = THUMBS[key]
    p = THUMB[theme_name]
    c = Canvas()
    thumb_background(c, p)
    draw(c, p)
    return svg(c, TW, TH, 4, label)


# --- Section icons (one version that reads on light and dark) ------------

ICON_COLORS = {
    "o": "#3b4a7a", "w": "#f5f7ff", "g": "#8b98b8", "Y": "#e3b341",
    "B": "#58a6ff", "P": "#a371f7", "G": "#3fb950", "R": "#f85149",
}

ICONS = {
    "now": [
        ".oooooooooooooo.",
        ".oggggggggggggo.",
        "..oooooooooooo..",
        "..owwwwwwwwwwo..",
        "...owYYYYYYwo...",
        "....owYYYYwo....",
        ".....owYYwo.....",
        "......oYYo......",
        "......owwo......",
        ".....owwYwo.....",
        "....owwwYwwo....",
        "...owwwYYYwwo...",
        "..owYYYYYYYYwo..",
        "..oooooooooooo..",
        ".oggggggggggggo.",
        ".oooooooooooooo.",
    ],
    "projects": [
        ".......oo.......",
        "......oYYo......",
        "......oYYo......",
        ".....oYYYYo.....",
        "oooooYYYYYYooooo",
        "oYYYYYYYYYYYYYYo",
        ".oYYYYYYYYYYYYo.",
        "..oYYYYYYYYYYo..",
        "...oYYYYYYYYo...",
        "...oYYYYYYYYo...",
        "..oYYYYooYYYYo..",
        "..oYYYo..oYYYo..",
        ".oYYYo....oYYYo.",
        ".oYYo......oYYo.",
        ".ooo........ooo.",
        "................",
    ],
    "stack": [
        "................",
        ".oooooooooooooo.",
        ".oBBBBBBBBBBBBo.",
        ".oBwwBBBBBBBGBo.",
        ".oBBBBBBBBBBBBo.",
        ".oooooooooooooo.",
        ".oPPPPPPPPPPPPo.",
        ".oPwwPPPPPPPGPo.",
        ".oPPPPPPPPPPPPo.",
        ".oooooooooooooo.",
        ".oggggggggggggo.",
        ".ogwwggggggggGo.",
        ".oggggggggggggo.",
        ".oooooooooooooo.",
        "................",
        "................",
    ],
    "beyond": [
        "................",
        "................",
        "................",
        "..oooo....oooo..",
        ".oPPPPooooPPPPo.",
        "oPPPPPPPPPPPPPPo",
        "oPPwPPPPPPPPRPPo",
        "oPwwwPPPPPPRPYPo",
        "oPPwPPPPPPPPGPPo",
        "oPPPPPPooPPPPPPo",
        "oPPPPPo..oPPPPPo",
        ".oPPPo....oPPPo.",
        "..ooo......ooo..",
        "................",
        "................",
        "................",
    ],
    "contact": [
        "................",
        "................",
        "................",
        ".oooooooooooooo.",
        ".oowwwwwwwwwwoo.",
        ".owowwwwwwwwowo.",
        ".owwowwwwwwowwo.",
        ".owwwowwwwowwwo.",
        ".owwwwoRRowwwwo.",
        ".owwwwwoowwwwwo.",
        ".owwwwwwwwwwwwo.",
        ".owwwwwwwwwwwwo.",
        ".oooooooooooooo.",
        "................",
        "................",
        "................",
    ],
}


def build_icon(key):
    c = Canvas()
    for y, row in enumerate(ICONS[key]):
        x = 0
        while x < len(row):
            ch = row[x]
            start = x
            while x < len(row) and row[x] == ch:
                x += 1
            if ch != ".":
                c.rect(start, y, x - start, 1, ICON_COLORS[ch])
    return svg(c, 16, 16, 2, "")


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent
    files = {}
    for theme in THEMES:
        files[f"banner-{theme}.svg"] = build_banner(theme)
        files[f"footer-{theme}.svg"] = build_footer(theme)
        for key in THUMBS:
            files[f"projects/{key}-{theme}.svg"] = build_thumb(key, theme)
    for key in ICONS:
        files[f"icons/{key}.svg"] = build_icon(key)
    for name, content in files.items():
        path = out / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"{path.stat().st_size:>7} bytes  {name}")
