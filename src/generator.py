import svgwrite
import math
from pathlib import Path

CATEGORY_COLORS = {
    "hiragana":    { "border": "#ffb3ac", "light": "#201515", "accent": "#d32f2f", "branch": "#ffb3ac" },
    "katakana":    { "border": "#00daf3", "light": "#0d2022", "accent": "#00daf3", "branch": "#00daf3" },
    "kanji":       { "border": "#bdc2ff", "light": "#141420", "accent": "#bdc2ff", "branch": "#bdc2ff" },
    "vocabulary":  { "border": "#4cd6ff", "light": "#0d2025", "accent": "#00e5ff", "branch": "#4cd6ff" },
    "grammar":     { "border": "#c5c0ff", "light": "#15142a", "accent": "#c5c0ff", "branch": "#c5c0ff" },
    "expressions": { "border": "#ffb3ac", "light": "#201515", "accent": "#d32f2f", "branch": "#ffb3ac" },
    "review":      { "border": "#908f9d", "light": "#181818", "accent": "#c6c5d4", "branch": "#908f9d" },
}

PAPER_BG = "#1a1a1a"
PAPER_BORDER = "#2a2a2a"
CARD_BG = "#1e1e1e"
TEXT_DARK = "#e5e2e1"
TEXT_MEDIUM = "#c6c5d4"
TEXT_LIGHT = "#908f9d"
TEXT_JAPANESE = "#e5e2e1"
TIP_BG = "#202020"
TIP_BORDER = "#353534"
TIP_TEXT = "#c6c5d4"

W, H = 900, 700

# ── Kana → Romaji ──

_HIRAGANA_TO_ROMAJI = {
    "あ": "a", "い": "i", "う": "u", "え": "e", "お": "o",
    "か": "ka", "き": "ki", "く": "ku", "け": "ke", "こ": "ko",
    "さ": "sa", "し": "shi", "す": "su", "せ": "se", "そ": "so",
    "た": "ta", "ち": "chi", "つ": "tsu", "て": "te", "と": "to",
    "な": "na", "に": "ni", "ぬ": "nu", "ね": "ne", "の": "no",
    "は": "ha", "ひ": "hi", "ふ": "fu", "へ": "he", "ほ": "ho",
    "ま": "ma", "み": "mi", "む": "mu", "め": "me", "も": "mo",
    "や": "ya", "ゆ": "yu", "よ": "yo",
    "ら": "ra", "り": "ri", "る": "ru", "れ": "re", "ろ": "ro",
    "わ": "wa", "を": "o", "ん": "n",
    "が": "ga", "ぎ": "gi", "ぐ": "gu", "げ": "ge", "ご": "go",
    "ざ": "za", "じ": "ji", "ず": "zu", "ぜ": "ze", "ぞ": "zo",
    "だ": "da", "ぢ": "ji", "づ": "zu", "で": "de", "ど": "do",
    "ば": "ba", "び": "bi", "ぶ": "bu", "べ": "be", "ぼ": "bo",
    "ぱ": "pa", "ぴ": "pi", "ぷ": "pu", "ぺ": "pe", "ぽ": "po",
    # Compounds
    "きゃ": "kya", "きゅ": "kyu", "きょ": "kyo",
    "しゃ": "sha", "しゅ": "shu", "しょ": "sho",
    "ちゃ": "cha", "ちゅ": "chu", "ちょ": "cho",
    "にゃ": "nya", "にゅ": "nyu", "にょ": "nyo",
    "ひゃ": "hya", "ひゅ": "hyu", "ひょ": "hyo",
    "みゃ": "mya", "みゅ": "myu", "みょ": "myo",
    "りゃ": "rya", "りゅ": "ryu", "りょ": "ryo",
    "ぎゃ": "gya", "ぎゅ": "gyu", "ぎょ": "gyo",
    "じゃ": "ja", "じゅ": "ju", "じょ": "jo",
    "びゃ": "bya", "びゅ": "byu", "びょ": "byo",
    "ぴゃ": "pya", "ぴゅ": "pyu", "ぴょ": "pyo",
}

_KATAKANA_TO_ROMAJI = {
    "ア": "a", "イ": "i", "ウ": "u", "エ": "e", "オ": "o",
    "カ": "ka", "キ": "ki", "ク": "ku", "ケ": "ke", "コ": "ko",
    "サ": "sa", "シ": "shi", "ス": "su", "セ": "se", "ソ": "so",
    "タ": "ta", "チ": "chi", "ツ": "tsu", "テ": "te", "ト": "to",
    "ナ": "na", "ニ": "ni", "ヌ": "nu", "ネ": "ne", "ノ": "no",
    "ハ": "ha", "ヒ": "hi", "フ": "fu", "ヘ": "he", "ホ": "ho",
    "マ": "ma", "ミ": "mi", "ム": "mu", "メ": "me", "モ": "mo",
    "ヤ": "ya", "ユ": "yu", "ヨ": "yo",
    "ラ": "ra", "リ": "ri", "ル": "ru", "レ": "re", "ロ": "ro",
    "ワ": "wa", "ヲ": "o", "ン": "n",
    "ガ": "ga", "ギ": "gi", "グ": "gu", "ゲ": "ge", "ゴ": "go",
    "ザ": "za", "ジ": "ji", "ズ": "zu", "ゼ": "ze", "ゾ": "zo",
    "ダ": "da", "ヂ": "ji", "ヅ": "zu", "デ": "de", "ド": "do",
    "バ": "ba", "ビ": "bi", "ブ": "bu", "ベ": "be", "ボ": "bo",
    "パ": "pa", "ピ": "pi", "プ": "pu", "ペ": "pe", "ポ": "po",
    # Compounds
    "キャ": "kya", "キュ": "kyu", "キョ": "kyo",
    "シャ": "sha", "シュ": "shu", "ショ": "sho",
    "チャ": "cha", "チュ": "chu", "チョ": "cho",
    "ニャ": "nya", "ニュ": "nyu", "ニョ": "nyo",
    "ヒャ": "hya", "ヒュ": "hyu", "ヒョ": "hyo",
    "ミャ": "mya", "ミュ": "myu", "ミョ": "myo",
    "リャ": "rya", "リュ": "ryu", "リョ": "ryo",
    "ギャ": "gya", "ギュ": "gyu", "ギョ": "gyo",
    "ジャ": "ja", "ジュ": "ju", "ジョ": "jo",
    "ビャ": "bya", "ビュ": "byu", "ビョ": "byo",
    "ピャ": "pya", "ピュ": "pyu", "ピョ": "pyo",
}

def _kana_to_romaji(text, kana_map):
    text = str(text or "")
    parts = []
    geminate = False
    i = 0
    while i < len(text):
        ch = text[i]
        # Long vowel mark ー → repeat previous vowel
        if ch == "ー":
            if parts:
                last = parts[-1]
                if last and last[-1] in "aiueo":
                    parts.append(last[-1])
                else:
                    parts.append("-")
            else:
                parts.append("-")
            i += 1
            continue
        if i + 1 < len(text):
            pair = text[i:i+2]
            if pair in kana_map:
                roma = kana_map[pair]
                if geminate and roma:
                    roma = roma[0] + roma
                    geminate = False
                parts.append(roma)
                i += 2
                continue
        if ch in ("っ", "ッ"):
            geminate = True
            i += 1
            continue
        if ch in ("ゃ", "ゅ", "ょ", "ャ", "ュ", "ョ"):
            i += 1
            continue
        roma = kana_map.get(ch, ch)
        if geminate and roma:
            roma = roma[0] + roma
            geminate = False
        parts.append(roma)
        i += 1
    return "".join(parts)

def _hira_to_romaji(text):
    return _kana_to_romaji(text, _HIRAGANA_TO_ROMAJI)

def _kata_to_romaji(text):
    return _kana_to_romaji(text, _KATAKANA_TO_ROMAJI)

# ── End Kana → Romaji ──


def _fit_text(text, max_chars):
    text = str(text or "")
    if len(text) <= max_chars:
        return text
    return text[:max(0, max_chars - 1)].rstrip() + "…"


def _wrap_text(text, max_chars, max_lines=2):
    text = " ".join(str(text or "").split())
    if not text:
        return []

    words = text.split(" ")
    lines = []
    current = ""
    for word in words:
        next_line = f"{current} {word}".strip()
        if len(next_line) <= max_chars:
            current = next_line
            continue
        if current:
            lines.append(current)
        current = word
        if len(lines) == max_lines:
            break

    if current and len(lines) < max_lines:
        lines.append(current)

    if len(lines) == max_lines and len(" ".join(words)) > len(" ".join(lines)):
        lines[-1] = _fit_text(lines[-1], max_chars)

    return lines


def _draw_text_lines(dwg, lines, x, y, line_h, fill, font_size, font_family, text_anchor="start", font_weight=None):
    for idx, line in enumerate(lines):
        kwargs = {
            "insert": (x, y + idx * line_h),
            "fill": fill,
            "font_size": str(font_size),
            "font_family": font_family,
            "text_anchor": text_anchor,
        }
        if font_weight:
            kwargs["font_weight"] = font_weight
        dwg.add(dwg.text(line, **kwargs))


# ── Helpers geométricos ──

def _radial_positions(cx, cy, n, radius_x, radius_y, start_angle=-90):
    positions = []
    for i in range(n):
        angle = start_angle + (360 / n) * i
        rad = math.radians(angle)
        x = cx + radius_x * math.cos(rad)
        y = cy + radius_y * math.sin(rad)
        positions.append((x, y, angle))
    return positions

def _semi_positions(cx, cy, n, radius_x, radius_y, spread=200, start=-110):
    positions = []
    if n <= 1:
        return [(cx, cy + radius_y, -90)]
    for i in range(n):
        angle = start + (spread / (n - 1)) * i if n > 1 else 0
        rad = math.radians(angle)
        x = cx + radius_x * math.cos(rad)
        y = cy + radius_y * math.sin(rad)
        positions.append((x, y, angle))
    return positions

def _grid_positions(start_x, start_y, cols, cell_w, cell_h, n):
    positions = []
    for i in range(n):
        col = i % cols
        row = i // cols
        x = start_x + col * cell_w
        y = start_y + row * cell_h
        positions.append((x, y))
    return positions


# ── Decoraciones SVG ──

def _add_gradient(dwg, name, c1, c2):
    grad = dwg.defs.add(dwg.linearGradient(id=name, x1="0%", y1="0%", x2="100%", y2="100%"))
    grad.add_stop_color(0.0, c1)
    grad.add_stop_color(1.0, c2)

def _add_paper_background(dwg):
    _add_gradient(dwg, "paper-grad", PAPER_BG, "#1e1e1e")
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), rx=16, fill="url(#paper-grad)"))
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), rx=16,
                      fill="none", stroke=PAPER_BORDER, stroke_width=1.5))

def _draw_sakura(dwg, x, y, size=20):
    group = dwg.add(dwg.g(opacity=0.35))
    for i in range(5):
        angle = math.radians(-90 + i * 72)
        px = x + size * 0.6 * math.cos(angle)
        py = y + size * 0.6 * math.sin(angle)
        group.add(dwg.circle(center=(px, py), r=size * 0.4, fill="#ffd5de"))
    group.add(dwg.circle(center=(x, y), r=size * 0.2, fill="#ffb7c5"))

def _draw_star(dwg, x, y, size=12):
    points = []
    for i in range(10):
        angle = math.radians(-90 + i * 36)
        r = size if i % 2 == 0 else size * 0.45
        points.append((x + r * math.cos(angle), y + r * math.sin(angle)))
    dwg.add(dwg.polygon(points=points, fill="#c4c7c7", opacity=0.4))

def _draw_cloud(dwg, x, y, size=25):
    g = dwg.add(dwg.g(opacity=0.2, fill="#d4d7d7"))
    g.add(dwg.circle(center=(x, y), r=size * 0.5))
    g.add(dwg.circle(center=(x - size * 0.4, y + size * 0.1), r=size * 0.35))
    g.add(dwg.circle(center=(x + size * 0.4, y + size * 0.1), r=size * 0.35))
    g.add(dwg.circle(center=(x + size * 0.1, y - size * 0.15), r=size * 0.3))

def _draw_sun(dwg, x, y, size=30):
    g = dwg.add(dwg.g(opacity=0.25))
    for i in range(8):
        angle = math.radians(-90 + i * 45)
        px = x + size * 0.7 * math.cos(angle)
        py = y + size * 0.7 * math.sin(angle)
        g.add(dwg.line(start=(x, y), end=(px, py), stroke="#d4d7d7", stroke_width=2))
    g.add(dwg.circle(center=(x, y), r=size * 0.4, fill="#e2e2e2"))

def _draw_fuji(dwg, x, y, size=40):
    g = dwg.add(dwg.g(opacity=0.18))
    path_data = f"M {x} {y+size} L {x-size*0.6} {y+size*0.3} L {x-size*0.35} {y+size*0.3} L {x} {y} L {x+size*0.35} {y+size*0.3} L {x+size*0.6} {y+size*0.3} Z"
    g.add(dwg.path(d=path_data, fill="#d4d7d7"))
    snow = f"M {x} {y+size*0.15} L {x-size*0.1} {y+size*0.3} L {x+size*0.1} {y+size*0.3} Z"
    g.add(dwg.path(d=snow, fill="#eeeeee"))

def _draw_cat_face(dwg, x, y, size=18):
    g = dwg.add(dwg.g(opacity=0.25))
    g.add(dwg.circle(center=(x, y), r=size, fill="#eeeeee"))
    g.add(dwg.polygon(points=[
        (x - size * 0.6, y + size * 0.2),
        (x - size * 0.9, y - size * 0.5),
        (x - size * 0.3, y - size * 0.1),
    ], fill="#eeeeee"))
    g.add(dwg.polygon(points=[
        (x + size * 0.6, y + size * 0.2),
        (x + size * 0.9, y - size * 0.5),
        (x + size * 0.3, y - size * 0.1),
    ], fill="#eeeeee"))
    g.add(dwg.line(start=(x - size * 0.2, y), end=(x - size * 0.05, y + size * 0.1), stroke="#c4c7c7", stroke_width=1))
    g.add(dwg.line(start=(x + size * 0.2, y), end=(x + size * 0.05, y + size * 0.1), stroke="#c4c7c7", stroke_width=1))
    g.add(dwg.line(start=(x - size * 0.15, y + size * 0.2), end=(x + size * 0.15, y + size * 0.2), stroke="#c4c7c7", stroke_width=1))

def _add_decorations(dwg, theme, seed=0):
    if theme in ("hiragana", "katakana", "review"):
        _draw_sakura(dwg, 60, 50, 18)
        _draw_sakura(dwg, 130, 70, 14)
        _draw_cloud(dwg, 800, 60, 30)
        _draw_cloud(dwg, 720, 100, 22)
        _draw_star(dwg, 50, 640, 14)
        _draw_star(dwg, 820, 620, 16)
        _draw_sakura(dwg, 830, 500, 16)
    elif theme == "kanji":
        _draw_sun(dwg, 780, 80, 35)
        _draw_fuji(dwg, 100, 580, 50)
        _draw_star(dwg, 50, 120, 12)
        _draw_star(dwg, 830, 650, 14)
    elif theme == "vocabulary":
        _draw_cat_face(dwg, 80, 620, 20)
        _draw_star(dwg, 100, 60, 14)
        _draw_star(dwg, 800, 60, 14)
        _draw_star(dwg, 50, 350, 10)
        _draw_star(dwg, 840, 350, 10)
        _draw_sun(dwg, 820, 620, 25)
    elif theme == "expressions":
        _draw_sakura(dwg, 70, 60, 16)
        _draw_sakura(dwg, 830, 60, 16)
        _draw_cat_face(dwg, 60, 610, 22)
        _draw_star(dwg, 820, 610, 14)
        _draw_cloud(dwg, 760, 80, 25)
    elif theme == "grammar":
        _draw_star(dwg, 60, 60, 14)
        _draw_cloud(dwg, 800, 50, 28)
        _draw_star(dwg, 830, 630, 14)
        _draw_cloud(dwg, 100, 630, 22)


# ── Componentes de mapa ──

def _draw_curved_branch(dwg, x1, y1, x2, y2, color, label=""):
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2 - 30
    d = f"M {x1},{y1} Q {mx},{my} {x2},{y2}"
    dwg.add(dwg.path(d=d, fill="none", stroke=color, stroke_width=2.5, stroke_linecap="round", opacity=0.5))
    dwg.add(dwg.path(d=d, fill="none", stroke=color, stroke_width=6, stroke_linecap="round", opacity=0.12))

def _draw_center_bubble(dwg, cx, cy, main_text, sub_text, sub_text2, color):
    colors = CATEGORY_COLORS.get(color, CATEGORY_COLORS["review"])
    border = colors["border"]
    light = colors["light"]

    dwg.add(dwg.circle(center=(cx, cy), r=74, fill=border, stroke="none", stroke_width=0, opacity=0.12))
    dwg.add(dwg.circle(center=(cx, cy), r=70, fill=light, stroke=border, stroke_width=3))
    dwg.add(dwg.circle(center=(cx, cy), r=62, fill=CARD_BG, stroke=border, stroke_width=1, stroke_opacity=0.5))

    lines = main_text.split("\n") if "\n" in str(main_text) else _wrap_text(main_text, 8, 2)
    line_h = 28 if len(lines) > 1 else 32
    total_h = len(lines) * line_h
    start_y = cy - total_h / 2 + line_h * 0.75

    _draw_text_lines(dwg, lines, cx, start_y, line_h, TEXT_JAPANESE, 25,
                     "'Noto Sans JP', 'Inter', sans-serif", text_anchor="middle", font_weight="bold")

    if sub_text:
        dwg.add(dwg.text(_fit_text(sub_text, 18), insert=(cx, cy + 36), text_anchor="middle",
                          fill=TEXT_MEDIUM, font_size="12",
                          font_family="Inter, sans-serif"))
    if sub_text2:
        dwg.add(dwg.text(_fit_text(sub_text2, 20), insert=(cx, cy + 54), text_anchor="middle",
                          fill=TEXT_LIGHT, font_size="9",
                          font_family="Inter, sans-serif"))

def _draw_numbered_card_simple(dwg, x, y, number, main_text, sub_text, translation, color):
    colors = CATEGORY_COLORS.get(color, CATEGORY_COLORS["review"])
    border = colors["border"]

    dwg.add(dwg.rect(insert=(x, y), size=(300, 68), rx=12, fill=CARD_BG,
                      stroke=border, stroke_width=1.5))
    dwg.add(dwg.circle(center=(x + 24, y + 34), r=14, fill=border))
    dwg.add(dwg.text(str(number), insert=(x + 24, y + 39), text_anchor="middle",
                      fill="white", font_size="12", font_weight="bold",
                      font_family="Inter, sans-serif"))

    main_text = _fit_text(main_text, 14)
    sub_text = _fit_text(sub_text, 28)

    dwg.add(dwg.text(main_text, insert=(x + 48, y + 24), fill=TEXT_JAPANESE, font_size="17",
                      font_weight="bold", font_family="'Noto Sans JP', 'Inter', sans-serif"))
    if sub_text:
        dwg.add(dwg.text(sub_text, insert=(x + 48, y + 46), fill=TEXT_MEDIUM, font_size="11",
                          font_family="Inter, sans-serif"))
    if translation:
        tx_offset = x + 48 + len(main_text) * 12 if main_text else x + 48
        if tx_offset < x + 260:
            romaji = _hira_to_romaji(translation) if any('\u3040' <= c <= '\u309f' for c in translation) else _kata_to_romaji(translation)
            dwg.add(dwg.text(f"= {translation}", insert=(tx_offset + 8, y + 22),
                              fill=TEXT_LIGHT, font_size="12",
                              font_family="'Noto Sans JP', Inter, sans-serif"))
            if romaji and romaji != translation:
                dwg.add(dwg.text(f"({romaji})", insert=(tx_offset + 8, y + 36),
                                  fill=TEXT_LIGHT, font_size="9",
                                  font_family="Inter, sans-serif"))

def _draw_numbered_card_kanji(dwg, x, y, number, kanji, reading, meaning, extra, color):
    colors = CATEGORY_COLORS.get(color, CATEGORY_COLORS["kanji"])
    border = colors["border"]

    dwg.add(dwg.rect(insert=(x, y), size=(320, 72), rx=12, fill=CARD_BG,
                      stroke=border, stroke_width=1.5))
    dwg.add(dwg.circle(center=(x + 22, y + 36), r=13, fill=border))
    dwg.add(dwg.text(str(number), insert=(x + 22, y + 41), text_anchor="middle",
                      fill="white", font_size="11", font_weight="bold",
                      font_family="Inter, sans-serif"))

    kanji = _fit_text(kanji, 3)
    reading = _fit_text(reading, 22)
    meaning = _fit_text(meaning, 24)
    extra = _fit_text(extra, 34)

    dwg.add(dwg.text(kanji, insert=(x + 46, y + 28), fill=TEXT_JAPANESE, font_size="20",
                      font_weight="bold", font_family="'Noto Sans JP', sans-serif"))
    dwg.add(dwg.text(reading, insert=(x + 92, y + 28), fill=TEXT_MEDIUM, font_size="10",
                      font_family="Inter, sans-serif"))
    dwg.add(dwg.text(meaning, insert=(x + 46, y + 52), fill=border, font_size="12",
                      font_weight="bold", font_family="Inter, sans-serif"))
    if extra:
        dwg.add(dwg.text(extra, insert=(x + 46, y + 66), fill=TEXT_LIGHT, font_size="9",
                          font_family="Inter, sans-serif"))

def _draw_numbered_card_vocab(dwg, x, y, number, japanese, reading, meaning, example, color):
    colors = CATEGORY_COLORS.get(color, CATEGORY_COLORS["vocabulary"])
    border = colors["border"]

    dwg.add(dwg.rect(insert=(x, y), size=(340, 78), rx=12, fill=CARD_BG,
                      stroke=border, stroke_width=1.5))
    dwg.add(dwg.circle(center=(x + 22, y + 39), r=13, fill=border))
    dwg.add(dwg.text(str(number), insert=(x + 22, y + 44), text_anchor="middle",
                      fill="white", font_size="11", font_weight="bold",
                      font_family="Inter, sans-serif"))

    japanese = _fit_text(japanese, 12)
    reading_raw = reading
    reading = _fit_text(reading, 22)
    meaning_lines = _wrap_text(meaning, 18, 2)
    example = _fit_text(example, 34)
    reading_romaji = _hira_to_romaji(reading_raw) if any('\u3040' <= c <= '\u309f' for c in reading_raw) else ""

    dwg.add(dwg.text(japanese, insert=(x + 46, y + 26), fill=TEXT_JAPANESE, font_size="17",
                      font_weight="bold", font_family="'Noto Sans JP', 'Inter', sans-serif"))
    if reading:
        dwg.add(dwg.text(reading, insert=(x + 46, y + 46), fill=TEXT_MEDIUM, font_size="11",
                          font_family="'Noto Sans JP', Inter, sans-serif"))
    if reading_romaji:
        dwg.add(dwg.text(reading_romaji, insert=(x + 46, y + 60), fill=TEXT_LIGHT, font_size="9",
                          font_family="Inter, sans-serif"))
    if meaning_lines:
        _draw_text_lines(dwg, meaning_lines, x + 200, y + 24, 14, TEXT_MEDIUM, 12,
                         "Inter, sans-serif")
    if example:
        dwg.add(dwg.text(example, insert=(x + 200, y + 50), fill=TEXT_LIGHT, font_size="9",
                          font_family="'Noto Sans JP', Inter, sans-serif"))

def _draw_numbered_card_expression(dwg, x, y, number, expression, reading, meaning, usage, color):
    colors = CATEGORY_COLORS.get(color, CATEGORY_COLORS["expressions"])
    border = colors["border"]

    dwg.add(dwg.rect(insert=(x, y), size=(260, 88), rx=12, fill=CARD_BG,
                      stroke=border, stroke_width=1.5))
    dwg.add(dwg.circle(center=(x + 20, y + 44), r=12, fill=border))
    dwg.add(dwg.text(str(number), insert=(x + 20, y + 49), text_anchor="middle",
                      fill="white", font_size="10", font_weight="bold",
                      font_family="Inter, sans-serif"))

    expression_lines = _wrap_text(expression, 18, 2)
    reading_raw = reading
    reading = _fit_text(reading, 30)
    meaning = _fit_text(meaning, 28)
    reading_romaji = _hira_to_romaji(reading_raw) if any('\u3040' <= c <= '\u309f' for c in reading_raw) else ""

    _draw_text_lines(dwg, expression_lines, x + 40, y + 24, 16, TEXT_JAPANESE, 15,
                     "'Noto Sans JP', 'Inter', sans-serif", font_weight="bold")
    if reading:
        dwg.add(dwg.text(reading, insert=(x + 12, y + 52), fill=TEXT_MEDIUM, font_size="10",
                          font_family="'Noto Sans JP', Inter, sans-serif"))
    if reading_romaji:
        dwg.add(dwg.text(reading_romaji, insert=(x + 12, y + 66), fill=TEXT_LIGHT, font_size="8",
                          font_family="Inter, sans-serif"))
    if meaning:
        dwg.add(dwg.text(meaning, insert=(x + 12, y + 80), fill=border, font_size="11",
                          font_weight="bold", font_family="Inter, sans-serif"))

def _draw_tip_box(dwg, tip_text, x, y, width, color):
    colors = CATEGORY_COLORS.get(color, CATEGORY_COLORS["review"])
    lines = _wrap_text(tip_text, int((width - 32) / 5.7), 2)
    height = 42 + max(1, len(lines)) * 14
    dwg.add(dwg.rect(insert=(x, y), size=(width, height), rx=10, fill=TIP_BG,
                      stroke=TIP_BORDER, stroke_width=1.5))
    dwg.add(dwg.text("💡 CONSEJO:", insert=(x + 14, y + 20), fill=TIP_TEXT, font_size="11",
                      font_weight="bold", font_family="Inter, sans-serif"))
    _draw_text_lines(dwg, lines, x + 14, y + 38, 14, TIP_TEXT, 10, "Inter, sans-serif")

def _draw_footer(dwg, topic_title, cy=680):
    dwg.add(dwg.line(start=(100, cy), end=(800, cy), stroke="#e2e2e2", stroke_width=1))
    dwg.add(dwg.text(_fit_text(topic_title, 90), insert=(450, cy + 14), text_anchor="middle",
                      fill=TEXT_LIGHT, font_size="11", font_family="Inter, sans-serif"))


# ── Generadores específicos ──

def generate_hiragana_map(topic, char_data, output_path):
    color = "hiragana"
    colors = CATEGORY_COLORS[color]
    chars = char_data.get("characters", [])[:5]

    positions = _semi_positions(450, 200, len(chars), 280, 200, spread=200, start=-100)
    min_y, max_y = 999, 0
    for x, y, angle in positions:
        cy2 = max(80, min(y, 520))
        min_y = min(min_y, cy2)
        max_y = max(max_y, cy2)

    tip_y = max_y + 50
    hira_h = max(H, tip_y + 120)
    dwg = svgwrite.Drawing(str(output_path), size=(W, hira_h), profile="tiny")
    _add_paper_background(dwg)
    _add_decorations(dwg, "hiragana")

    cx, cy = 450, 200
    row_chars = "".join(c.get("character", "") for c in chars)
    _draw_center_bubble(dwg, cx, cy, row_chars, char_data.get("label", ""), topic, color)

    tips = {
        "a-row": "Practica leyendo cada sonido en voz alta: あ (a), い (i), う (u), え (e), お (o).",
        "ka-row": "Los sonidos KA, KI, KU, KE, KO son la base de muchas palabras.",
        "sa-row": "し (shi) suena como 'shi' en inglés, no 'si' en español.",
        "ta-row": "ち (chi) y つ (tsu) son sonidos que no existen en español.",
        "na-row": "の (no) es la partícula posesiva más común del japonés.",
        "ha-row": "は (ha) como partícula se pronuncia 'wa'.",
        "ma-row": "La fila MA tiene sonidos suaves y redondeados.",
        "ya-row": "や (ya), ゆ (yu), よ (yo) son sonidos cortos y claros.",
        "ra-row": "ら (ra) suena entre 'ra', 'la' y 'da'.",
        "wa-row": "ん (n) es la única consonante sola en hiragana.",
    }
    tip = tips.get(char_data.get("id", ""), "Repite cada carácter 10 veces con su sonido.")

    for i, (x, y, angle) in enumerate(positions):
        cx2 = max(160, min(x, 740))
        cy2 = max(80, min(y, 520))
        _draw_curved_branch(dwg, cx, cy, cx2, cy2, colors["branch"])
        ch = chars[i]
        _draw_numbered_card_simple(dwg, cx2 - 150, cy2 - 31, i + 1, ch.get("character", ""),
                                    f"({ch.get('romaji', '')})",
                                    ch.get("examples", [{}])[0].get("word", ""), color)

    footer_cy = tip_y + 70
    _draw_tip_box(dwg, tip, 60, tip_y, 780, color)
    _draw_footer(dwg, topic, cy=footer_cy)
    dwg.save()
    _export_png(output_path)


def generate_katakana_map(topic, char_data, output_path):
    color = "katakana"
    colors = CATEGORY_COLORS[color]
    chars = char_data.get("characters", [])[:5]

    positions = _semi_positions(450, 200, len(chars), 280, 200, spread=200, start=-100)
    min_y, max_y = 999, 0
    for x, y, angle in positions:
        cy2 = max(80, min(y, 520))
        min_y = min(min_y, cy2)
        max_y = max(max_y, cy2)

    tip_y = max_y + 50
    kata_h = max(H, tip_y + 120)
    dwg = svgwrite.Drawing(str(output_path), size=(W, kata_h), profile="tiny")
    _add_paper_background(dwg)
    _add_decorations(dwg, "katakana")

    cx, cy = 450, 200
    row_chars = "".join(c.get("character", "") for c in chars)
    _draw_center_bubble(dwg, cx, cy, row_chars, char_data.get("label", ""), topic, color)

    tips = {
        "a-row": "Katakana se usa para palabras extranjeras: コーヒー, パン, テレビ.",
        "ka-row": "カメラ (kamera), カレー (karē)... muchas palabras vienen del inglés.",
        "sa-row": "サッカー (sakkā), サラダ (sarada) — palabras internacionales.",
        "ta-row": "タクシー (takushī), テーブル (tēburu) — préstamos del inglés.",
        "na-row": "ナイフ (naifu), ノート (nōto) — útiles para el estudio.",
        "ha-row": "ホテル (hoteru), ハンバーガー (hanbāgā) — comida internacional.",
        "ma-row": "マンガ (manga), メール (mēru) — japonés moderno.",
        "ya-row": "ヤクザ (yakuza), ヨガ (yoga) — palabras japonesas famosas.",
        "ra-row": "ラーメン (rāmen), レモン (remon) — comida deliciosa.",
        "wa-row": "ワイン (wain), オンライン (onrain) — tecnología y cultura.",
    }
    tip = tips.get(char_data.get("id", ""), "Compara cada katakana con su versión en hiragana.")

    for i, (x, y, angle) in enumerate(positions):
        cx2 = max(160, min(x, 740))
        cy2 = max(80, min(y, 520))
        _draw_curved_branch(dwg, cx, cy, cx2, cy2, colors["branch"])
        ch = chars[i]
        _draw_numbered_card_simple(dwg, cx2 - 150, cy2 - 31, i + 1, ch.get("character", ""),
                                    f"({ch.get('romaji', '')})",
                                    ch.get("examples", [{}])[0].get("word", ""), color)

    footer_cy = tip_y + 70
    _draw_tip_box(dwg, tip, 60, tip_y, 780, color)
    _draw_footer(dwg, topic, cy=footer_cy)
    dwg.save()
    _export_png(output_path)


def generate_kanji_map(topic, theme_data, output_path):
    color = "kanji"
    colors = CATEGORY_COLORS[color]
    items = theme_data.get("items", [])[:10]
    n = len(items)
    cols = 2 if n > 4 else 1
    rows = (n + cols - 1) // cols
    cell_w = 340
    cell_h = 80
    grid_w = cols * cell_w
    start_x = (W - grid_w) / 2
    grid_top = max(235, 130 + rows * 15)
    grid_bottom = grid_top + rows * cell_h
    kanji_h = grid_bottom + 200
    tip_y = grid_bottom + 25

    dwg = svgwrite.Drawing(str(output_path), size=(W, kanji_h), profile="tiny")
    _add_paper_background(dwg)
    _add_decorations(dwg, "kanji")

    _draw_center_bubble(dwg, W / 2, max(120, 300 - rows * 25), "漢字", theme_data.get("label", ""), topic, color)

    for i, item in enumerate(items):
        col = i % cols
        row = i // cols
        x = start_x + col * cell_w
        y = grid_top + row * cell_h

        kanji = item.get("kanji", "")
        reading = item.get("reading", "")
        meaning = item.get("meaning", "")
        radical = item.get("radical", "")
        strokes = item.get("strokes", "")
        extra = f"Radical: {radical} · {strokes} trazos" if radical and strokes else ""

        _draw_curved_branch(dwg, W / 2, max(120, 300 - rows * 25), x + 60, y + 36, colors["branch"])
        _draw_numbered_card_kanji(dwg, x, y, i + 1, kanji, reading, meaning, extra, color)

    tips = {
        "numbers": "Aprende el orden de trazos: cada kanji tiene un orden específico.",
        "nature": "Muchos kanji de naturaleza vienen de pictogramas (日月木山川).",
        "people": "人 parece una persona caminando. 女 y 男 muestran género.",
        "places": "上 (arriba) y 下 (abajo) son opuestos fáciles de recordar.",
        "school": "学 y 校 juntos forman 学校 (escuela). Practica combinaciones.",
    }
    tip = tips.get(theme_data.get("id", ""), "Estudia los radicales para memorizar kanji más rápido.")
    _draw_tip_box(dwg, tip, 60, tip_y, 780, color)
    _draw_footer(dwg, topic, cy=kanji_h - 30)
    dwg.save()
    _export_png(output_path)


def generate_vocabulary_map(topic, theme_data, output_path):
    color = "vocabulary"
    colors = CATEGORY_COLORS[color]
    items = theme_data.get("items", [])[:10]
    n = len(items)
    cols = 2
    cell_w = 370
    cell_h = 80
    start_x = (W - cols * cell_w) / 2
    start_y = 210
    grid_bottom = start_y + ((n - 1) // cols + 1) * cell_h
    tip_y = grid_bottom + 20
    vocab_h = max(H, tip_y + 100)
    dwg = svgwrite.Drawing(str(output_path), size=(W, vocab_h), profile="tiny")
    _add_paper_background(dwg)
    _add_decorations(dwg, "vocabulary")

    cx = 450
    label = theme_data.get("label", topic.replace("Vocabulario: ", ""))
    _draw_center_bubble(dwg, cx, 130, label, "Vocabulario", topic, color)

    for i, item in enumerate(items):
        col = i % cols
        row = i // cols
        x = start_x + col * cell_w
        y = start_y + row * cell_h

        jp = item.get("japanese", "")
        reading = item.get("reading", "")
        meaning = item.get("meaning", "")
        example = item.get("example", "")

        _draw_numbered_card_vocab(dwg, x, y, i + 1, jp, reading, meaning, example, color)

    tips = {
        "colors": "  Usa 色 (iro) para preguntar colores: 何色？(naniiro?)",
        "animals": "  Animales domésticos: 犬 (perro), 猫 (gato). ¿Tienes mascota?",
        "food": "  いただきます antes de comer, ごちそうさま después.",
        "family": "  Japonés distingue familia propia vs. ajena. ¡Cuidado!",
        "weather": "  天気 (tenki) es clima. 今日の天気は？(¿Cómo está el clima hoy?)",
        "time": "  La semana empieza en domingo en Japón (日曜日).",
        "body": "  頭 (atama), 顔 (kao), 手 (te) — partes básicas del cuerpo.",
        "greetings": "  こんにちは se usa de 11am a 5pm aproximadamente.",
        "adjectives_i": "  Los adjetivos-I terminan en い y se conjugan (大きい→大きくない).",
    }
    tip = tips.get(theme_data.get("id", ""), "Usa vocabulario nuevo en frases cada día.")
    footer_cy = tip_y + 85
    _draw_tip_box(dwg, tip, 60, tip_y, 780, color)
    _draw_footer(dwg, topic, cy=footer_cy)
    dwg.save()
    _export_png(output_path)


def generate_grammar_map(topic, topic_data, output_path):
    color = "grammar"
    colors = CATEGORY_COLORS[color]
    examples = topic_data.get("examples", [])[:4]
    n_examples = len(examples)
    tip_y = 100 + n_examples * 145 + 20
    grammar_h = max(H, tip_y + 120)

    dwg = svgwrite.Drawing(str(output_path), size=(W, grammar_h), profile="tiny")
    _add_paper_background(dwg)
    _add_decorations(dwg, "grammar")

    cx, cy = 220, 300
    label = topic_data.get("label", topic)
    structure = topic_data.get("structure", "")
    _draw_center_bubble(dwg, cx, cy, label, structure, "", color)

    for i, ex in enumerate(examples):
        x, y = 380, 100 + i * 145

        _draw_curved_branch(dwg, cx + 70, cy + (i - 1.5) * 30, x, y + 50, colors["branch"])

        dwg.add(dwg.rect(insert=(x, y), size=(480, 120), rx=12, fill=CARD_BG,
                          stroke=colors["border"], stroke_width=1.5))

        japanese_lines = _wrap_text(ex.get("japanese", ""), 28, 2)
        reading = ex.get("reading", "")
        reading_romaji = _hira_to_romaji(reading) if any('\u3040' <= c <= '\u309f' for c in reading) else ""
        reading_display = _fit_text(reading, 38)
        meaning_lines = _wrap_text(ex.get("meaning", ""), 48, 2)
        _draw_text_lines(dwg, japanese_lines, x + 16, y + 27, 22, TEXT_JAPANESE, 18,
                         "'Noto Sans JP', 'Inter', sans-serif", font_weight="bold")
        if reading_display:
            dwg.add(dwg.text(reading_display, insert=(x + 16, y + 58), fill=TEXT_MEDIUM,
                              font_size="11", font_family="'Noto Sans JP', Inter, sans-serif"))
        if reading_romaji:
            dwg.add(dwg.text(reading_romaji, insert=(x + 16, y + 72), fill=TEXT_LIGHT,
                              font_size="9", font_family="Inter, sans-serif"))
        _draw_text_lines(dwg, meaning_lines, x + 16, y + 90, 15, colors["accent"], 13,
                         "Inter, sans-serif", font_weight="bold")

    footer_cy = tip_y + 80
    _draw_tip_box(dwg, topic_data.get("usage", topic), 60, tip_y, 780, color)

    _draw_footer(dwg, topic, cy=footer_cy)
    dwg.save()
    _export_png(output_path)


def generate_expressions_map(topic, cat_data, output_path):
    color = "expressions"
    colors = CATEGORY_COLORS[color]
    items = cat_data.get("items", [])[:9]
    n = len(items)
    cols = 3
    cell_w = 275
    cell_h = 95
    start_x = (W - cols * cell_w) / 2
    start_y = 195
    grid_bottom = start_y + ((n - 1) // cols + 1) * cell_h
    tip_y = grid_bottom + 15
    expr_h = max(H, tip_y + 120)

    dwg = svgwrite.Drawing(str(output_path), size=(W, expr_h), profile="tiny")
    _add_paper_background(dwg)
    _add_decorations(dwg, "expressions")

    label = cat_data.get("label", topic.replace("Expresiones: ", ""))
    _draw_center_bubble(dwg, 450, 120, label, "Expresiones", topic, color)

    n = len(items)
    cols = 3
    cell_w = 275
    cell_h = 95
    start_x = (W - cols * cell_w) / 2
    start_y = 195
    grid_bottom = start_y + ((n - 1) // cols + 1) * cell_h
    tip_y = grid_bottom + 15

    for i, item in enumerate(items):
        col = i % cols
        row = i // cols
        x = start_x + col * cell_w
        y = start_y + row * cell_h

        _draw_numbered_card_expression(dwg, x, y, i + 1,
                                        item.get("expression", ""),
                                        item.get("reading", ""),
                                        item.get("meaning", ""),
                                        item.get("usage", ""),
                                        color)

    tips = {
        "basic-greetings": "  Usa こんにちは hasta el atardecer, luego こんばんは.",
        "politeness": "  Añadir ございます hace cualquier saludo más formal.",
        "restaurant": "  お願いします es la forma más educada de pedir.",
        "shopping": "  いくらですか？es la frase más útil para comprar.",
        "directions": "  すみません es perfecto para llamar la atención de alguien.",
        "emergencies": "  助けて！(tasukete!) es la palabra clave en emergencias.",
        "casual": "  Las expresiones casuales solo con amigos cercanos.",
    }
    tip = tips.get(cat_data.get("id", ""), "Usa estas expresiones en contexto para recordarlas mejor.")
    footer_cy = tip_y + 85
    _draw_tip_box(dwg, tip, 60, tip_y, 780, color)
    _draw_footer(dwg, topic, cy=footer_cy)
    dwg.save()
    _export_png(output_path)


def generate_review_map(topic, data_wrapper, output_path):
    review_type = data_wrapper.get("type", "") if isinstance(data_wrapper, dict) else ""
    all_data = data_wrapper.get("data", {}) if isinstance(data_wrapper, dict) else data_wrapper

    items = []
    if isinstance(all_data, dict):
        for key in ("items", "characters", "topics", "categories"):
            data = all_data.get(key, [])
            if data:
                items = data[:12]
                break

    n = len(items)
    cols = 3
    cell_w = 260
    cell_h = 65
    start_x = (W - cols * cell_w) / 2
    start_y = 180
    grid_bottom = start_y + ((n - 1) // cols + 1) * cell_h
    tip_y = grid_bottom + 15
    rev_h = max(H, tip_y + 120)

    dwg = svgwrite.Drawing(str(output_path), size=(W, rev_h), profile="tiny")
    _add_paper_background(dwg)
    _add_decorations(dwg, "review")

    rev_colors = CATEGORY_COLORS["review"]

    for i, item in enumerate(items):
        col = i % cols
        row = i // cols
        x = start_x + col * cell_w
        y = start_y + row * cell_h

        main = item.get("character") or item.get("kanji") or item.get("japanese") or item.get("expression") or ""
        sub = item.get("romaji") or item.get("reading") or item.get("meaning") or ""

        dwg.add(dwg.rect(insert=(x, y), size=(cell_w - 10, cell_h - 5), rx=8, fill=CARD_BG,
                          stroke=rev_colors["border"], stroke_width=1, stroke_opacity=0.5))
        main = _fit_text(main, 24)
        sub = _fit_text(sub, 34)

        dwg.add(dwg.text(main, insert=(x + 14, y + 24), fill=TEXT_JAPANESE, font_size="15",
                          font_weight="bold", font_family="'Noto Sans JP', 'Inter', sans-serif"))
        if sub:
            dwg.add(dwg.text(sub, insert=(x + 14, y + 46), fill=TEXT_MEDIUM, font_size="10",
                              font_family="Inter, sans-serif"))

    tip = "Revisa cada día lo aprendido para fijar el conocimiento a largo plazo."
    footer_cy = tip_y + 80
    _draw_tip_box(dwg, tip, 60, tip_y, 780, "review")
    _draw_footer(dwg, topic, cy=footer_cy)
    dwg.save()
    _export_png(output_path)


# ── Exportación PNG ──

def _export_png(svg_path):
    try:
        import cairosvg
        png_path = svg_path.with_suffix(".png")
        cairosvg.svg2png(url=str(svg_path), write_to=str(png_path), scale=2)
    except ImportError:
        pass
    except Exception:
        pass


# ── Registro de generadores ──

GENERATORS = {
    "hiragana": generate_hiragana_map,
    "katakana": generate_katakana_map,
    "kanji": generate_kanji_map,
    "vocabulary": generate_vocabulary_map,
    "grammar": generate_grammar_map,
    "expressions": generate_expressions_map,
    "review": generate_review_map,
}


def generate(category, topic, data, output_path):
    fn = GENERATORS.get(category, generate_review_map)
    fn(topic, data, output_path)
