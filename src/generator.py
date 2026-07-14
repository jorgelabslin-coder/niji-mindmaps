import svgwrite
import hashlib
from pathlib import Path

CATEGORY_COLORS = {
    "hiragana": { "primary": "#f472b6", "secondary": "#f9a8d4", "accent": "#ec4899" },
    "katakana": { "primary": "#60a5fa", "secondary": "#93bbfc", "accent": "#3b82f6" },
    "kanji":    { "primary": "#fbbf24", "secondary": "#fcd34d", "accent": "#f59e0b" },
    "vocabulary": { "primary": "#4ade80", "secondary": "#86efac", "accent": "#22c55e" },
    "grammar":  { "primary": "#a78bfa", "secondary": "#c4b5fd", "accent": "#8b5cf6" },
    "expressions": { "primary": "#fb923c", "secondary": "#fdba74", "accent": "#f97316" },
    "review":   { "primary": "#38bdf8", "secondary": "#7dd3fc", "accent": "#0ea5e9" },
}

def _colors(category):
    c = CATEGORY_COLORS.get(category, CATEGORY_COLORS["review"])
    return c["primary"], c["secondary"], c["accent"]

def generate_hiragana_map(topic, char_data, output_path):
    prim, sec, acc = _colors("hiragana")
    chars = char_data.get("characters", [])
    dwg = svgwrite.Drawing(str(output_path), size=("800", "600"), profile="tiny")

    bg = dwg.add(dwg.rect(insert=(0,0), size=("100%","100%"), fill="#0d0d18", rx=16))
    _add_gradient(dwg, "hiragana-bg", "#0d0d18", "#111128")
    bg.fill = "url(#hiragana-bg)"

    cx, cy = 400, 180
    _draw_center(dwg, chars[0]["character"] if chars else "あ", cx, cy, prim)

    items = chars[:5]
    angles = [-120, -60, 0, 60, 120]
    for i, ch in enumerate(items):
        rad = 3.14159 * angles[i] / 180
        x = cx + 220 * 1.2
        y = cy + 180 * 1.2

    _draw_branches(dwg, cx, cy, items, prim, sec)

    dwg.add(dwg.text(topic, insert=(400, 520), text_anchor="middle",
                      fill="#94a3b8", font_size="14", font_family="Inter, sans-serif"))
    dwg.add(dwg.text("niji-mindmaps", insert=(400, 560), text_anchor="middle",
                      fill="#334155", font_size="11", font_family="Inter, sans-serif"))
    dwg.save()

def _add_gradient(dwg, name, c1, c2):
    gradient = dwg.defs.add(dwg.linearGradient(id=name, x1="0%", y1="0%", x2="100%", y2="100%"))
    gradient.add_stop_color(0.0, c1)
    gradient.add_stop_color(1.0, c2)

def _draw_center(dwg, text, x, y, color):
    circle = dwg.add(dwg.circle(center=(x, y), r=45, fill=color, opacity=0.15))
    circle2 = dwg.add(dwg.circle(center=(x, y), r=38, fill=color, opacity=0.3))
    dwg.add(dwg.text(text, insert=(x, y+8), text_anchor="middle",
                      fill="#f1f5f9", font_size="28", font_weight="bold",
                      font_family="'Noto Sans JP', sans-serif"))

def _draw_branches(dwg, cx, cy, items, primary, secondary):
    for i, item in enumerate(items):
        angle = -120 + i * 60
        rad = angle * 3.14159 / 180
        bx = cx + 230 * 1.3
        by = cy + 180 * 1.3
        bx = min(max(bx, 80), 720)
        by = min(max(by, 40), 560)

        if i == 0:
            x, y = cx + 140, cy - 130
        elif i == 1:
            x, y = cx + 260, cy - 80
        elif i == 2:
            x, y = cx + 260, cy + 80
        elif i == 3:
            x, y = cx + 140, cy + 130
        else:
            x, y = cx - 120, cy

        dwg.add(dwg.line(start=(cx, cy), end=(x, y),
                          stroke=primary, stroke_width=2, opacity=0.4))

        node = dwg.add(dwg.rect(insert=(x-85, y-35), size=(170, 70), rx=10,
                                 fill="#0d0d18", stroke=primary, stroke_width=1, stroke_opacity=0.3))

        char = item.get("character", "")
        romaji = item.get("romaji", "")
        examples = item.get("examples", [])
        ex_text = ""
        if examples:
            ex_text = examples[0].get("word", "")

        dwg.add(dwg.text(char, insert=(x-70, y-8), fill="#f1f5f9", font_size="22",
                          font_family="'Noto Sans JP', sans-serif"))
        dwg.add(dwg.text(f"({romaji})", insert=(x-30, y-8), fill="#64748b", font_size="12",
                          font_family="Inter, sans-serif"))
        if ex_text:
            dwg.add(dwg.text(ex_text, insert=(x-70, y+18), fill="#94a3b8", font_size="11",
                              font_family="'Noto Sans JP', sans-serif"))

def generate_katakana_map(topic, char_data, output_path):
    prim, sec, acc = _colors("katakana")
    chars = char_data.get("characters", [])
    dwg = svgwrite.Drawing(str(output_path), size=("800", "600"), profile="tiny")

    _add_gradient(dwg, "kata-bg", "#0d0d18", "#0a1628")
    dwg.add(dwg.rect(insert=(0,0), size=("100%","100%"), rx=16, fill="url(#kata-bg)"))

    cx, cy = 400, 200
    _draw_center_kata(dwg, chars[0]["character"] if chars else "ア", cx, cy, prim)

    for i, ch in enumerate(chars[:5]):
        if i == 0:
            x, y = cx + 140, cy - 130
        elif i == 1:
            x, y = cx + 260, cy - 80
        elif i == 2:
            x, y = cx + 260, cy + 80
        elif i == 3:
            x, y = cx + 140, cy + 130
        else:
            x, y = cx - 120, cy

        dwg.add(dwg.line(start=(cx, cy), end=(x, y),
                          stroke=prim, stroke_width=2, opacity=0.4))

        node = dwg.add(dwg.rect(insert=(x-85, y-35), size=(170, 70), rx=10,
                                 fill="#0d0d18", stroke=prim, stroke_width=1, stroke_opacity=0.3))

        char = ch.get("character", "")
        romaji = ch.get("romaji", "")
        examples = ch.get("examples", [])
        ex_text = examples[0].get("word", "") if examples else ""

        dwg.add(dwg.text(char, insert=(x-70, y-8), fill="#f1f5f9", font_size="22",
                          font_family="'Noto Sans JP', sans-serif"))
        dwg.add(dwg.text(f"({romaji})", insert=(x-30, y-8), fill="#64748b", font_size="12",
                          font_family="Inter, sans-serif"))
        if ex_text:
            dwg.add(dwg.text(ex_text, insert=(x-70, y+18), fill="#94a3b8", font_size="11",
                              font_family="'Noto Sans JP', sans-serif"))

    dwg.add(dwg.text(topic, insert=(400, 520), text_anchor="middle",
                      fill="#94a3b8", font_size="14", font_family="Inter, sans-serif"))
    dwg.add(dwg.text("niji-mindmaps", insert=(400, 560), text_anchor="middle",
                      fill="#334155", font_size="11", font_family="Inter, sans-serif"))
    dwg.save()

def _draw_center_kata(dwg, text, x, y, color):
    dwg.add(dwg.circle(center=(x, y), r=45, fill=color, opacity=0.15))
    dwg.add(dwg.circle(center=(x, y), r=38, fill=color, opacity=0.3))
    dwg.add(dwg.text(text, insert=(x, y+8), text_anchor="middle",
                      fill="#f1f5f9", font_size="28", font_weight="bold",
                      font_family="'Noto Sans JP', sans-serif"))

def generate_kanji_map(topic, theme_data, output_path):
    prim, sec, acc = _colors("kanji")
    items = theme_data.get("items", [])
    dwg = svgwrite.Drawing(str(output_path), size=("800", "600"), profile="tiny")

    _add_gradient(dwg, "kanji-bg", "#0d0d18", "#1a1208")
    dwg.add(dwg.rect(insert=(0,0), size=("100%","100%"), rx=16, fill="url(#kanji-bg)"))

    cx, cy = 400, 180
    _draw_center_kata(dwg, "漢字", cx, cy, prim)

    for i, item in enumerate(items[:6]):
        if i == 0:
            x, y = cx + 160, cy - 140
        elif i == 1:
            x, y = cx + 260, cy - 80
        elif i == 2:
            x, y = cx + 260, cy
        elif i == 3:
            x, y = cx + 260, cy + 80
        elif i == 4:
            x, y = cx + 160, cy + 140
        else:
            x, y = cx - 160, cy

        dwg.add(dwg.line(start=(cx, cy), end=(x, y),
                          stroke=prim, stroke_width=2, opacity=0.4))

        node = dwg.add(dwg.rect(insert=(x-95, y-40), size=(190, 80), rx=10,
                                 fill="#0d0d18", stroke=prim, stroke_width=1, stroke_opacity=0.3))

        kanji = item.get("kanji", "")
        meaning = item.get("meaning", "")
        reading = item.get("reading", "")
        examples = item.get("examples", [])
        ex_word = examples[0].get("word", "") if examples else ""
        ex_reading = examples[0].get("reading", "") if examples else ""
        ex_meaning = examples[0].get("meaning", "") if examples else ""

        dwg.add(dwg.text(kanji, insert=(x-80, y-12), fill="#f1f5f9", font_size="24",
                          font_family="'Noto Sans JP', sans-serif"))
        dwg.add(dwg.text(meaning, insert=(x-45, y-12), fill="#64748b", font_size="11",
                          font_family="Inter, sans-serif"))
        dwg.add(dwg.text(reading, insert=(x-80, y+12), fill="#fbbf24", font_size="10",
                          font_family="Inter, sans-serif"))
        if ex_word:
            dwg.add(dwg.text(f"{ex_word} = {ex_meaning}", insert=(x-80, y+30), fill="#94a3b8", font_size="10",
                              font_family="'Noto Sans JP', sans-serif"))

    dwg.add(dwg.text(topic, insert=(400, 545), text_anchor="middle",
                      fill="#94a3b8", font_size="14", font_family="Inter, sans-serif"))
    dwg.save()

def generate_vocabulary_map(topic, theme_data, output_path):
    prim, sec, acc = _colors("vocabulary")
    items = theme_data.get("items", [])
    dwg = svgwrite.Drawing(str(output_path), size=("800", "600"), profile="tiny")

    _add_gradient(dwg, "voc-bg", "#0d0d18", "#081a0e")
    dwg.add(dwg.rect(insert=(0,0), size=("100%","100%"), rx=16, fill="url(#voc-bg)"))

    cx, cy = 400, 160
    title_text = topic.replace("Vocabulario: ", "")
    dwg.add(dwg.circle(center=(cx, cy), r=42, fill=prim, opacity=0.15))
    dwg.add(dwg.circle(center=(cx, cy), r=35, fill=prim, opacity=0.3))
    dwg.add(dwg.text(title_text, insert=(cx, cy+5), text_anchor="middle",
                      fill="#f1f5f9", font_size="18", font_weight="bold",
                      font_family="Inter, sans-serif"))

    for i, item in enumerate(items[:8]):
        col = i % 2
        row = i // 2
        x = 80 + col * 360
        y = 260 + row * 90

        card = dwg.add(dwg.rect(insert=(x, y), size=(340, 75), rx=10,
                                 fill="#0d0d18", stroke=prim, stroke_width=1, stroke_opacity=0.2))

        jp = item.get("japanese", "")
        reading = item.get("reading", "")
        meaning = item.get("meaning", "")
        example = item.get("example", "")

        dwg.add(dwg.text(jp, insert=(x+15, y+25), fill="#f1f5f9", font_size="16",
                          font_family="'Noto Sans JP', sans-serif"))
        dwg.add(dwg.text(f"({reading})", insert=(x+15, y+45), fill="#64748b", font_size="11",
                          font_family="Inter, sans-serif"))
        dwg.add(dwg.text(meaning, insert=(x+180, y+25), fill="#94a3b8", font_size="13",
                          font_family="Inter, sans-serif"))
        if example:
            dwg.add(dwg.text(example[:40], insert=(x+180, y+48), fill="#64748b", font_size="9",
                              font_family="'Noto Sans JP', sans-serif"))

    dwg.add(dwg.text(topic, insert=(400, 580), text_anchor="middle",
                      fill="#94a3b8", font_size="13", font_family="Inter, sans-serif"))
    dwg.save()

def generate_grammar_map(topic, topic_data, output_path):
    prim, sec, acc = _colors("grammar")
    dwg = svgwrite.Drawing(str(output_path), size=("800", "600"), profile="tiny")

    _add_gradient(dwg, "gram-bg", "#0d0d18", "#140e20")
    dwg.add(dwg.rect(insert=(0,0), size=("100%","100%"), rx=16, fill="url(#gram-bg)"))

    cx, cy = 180, 280
    label = topic_data.get("label", "")
    dwg.add(dwg.circle(center=(cx, cy), r=55, fill=prim, opacity=0.15))
    dwg.add(dwg.circle(center=(cx, cy), r=45, fill=prim, opacity=0.3))
    dwg.add(dwg.text(label, insert=(cx, cy-8), text_anchor="middle",
                      fill="#f1f5f9", font_size="14", font_weight="bold",
                      font_family="Inter, sans-serif"))
    dwg.add(dwg.text(topic_data.get("structure", ""), insert=(cx, cy+18), text_anchor="middle",
                      fill="#94a3b8", font_size="11",
                      font_family="Inter, sans-serif"))

    examples = topic_data.get("examples", [])
    for i, ex in enumerate(examples[:3]):
        x, y = 380, 140 + i * 150

        arrow = dwg.add(dwg.line(start=(245, 260 + i * 50), end=(370, 140 + i * 150),
                                  stroke=prim, stroke_width=2, opacity=0.3))

        card = dwg.add(dwg.rect(insert=(x, y), size=(380, 120), rx=10,
                                 fill="#0d0d18", stroke=prim, stroke_width=1, stroke_opacity=0.2))

        dwg.add(dwg.text(ex.get("japanese", ""), insert=(x+15, y+30), fill="#f1f5f9", font_size="16",
                          font_family="'Noto Sans JP', sans-serif"))
        dwg.add(dwg.text(ex.get("reading", ""), insert=(x+15, y+55), fill="#64748b", font_size="12",
                          font_family="Inter, sans-serif"))
        dwg.add(dwg.text(ex.get("meaning", ""), insert=(x+15, y+85), fill="#a78bfa", font_size="13",
                          font_family="Inter, sans-serif"))
        dwg.add(dwg.text(f"Ejemplo {i+1}", insert=(x+15, y+110), fill="#334155", font_size="9",
                          font_family="Inter, sans-serif"))

    usage = topic_data.get("usage", "")
    if usage:
        dwg.add(dwg.text(f"Uso: {usage}", insert=(400, 560), text_anchor="middle",
                          fill="#94a3b8", font_size="11", font_family="Inter, sans-serif"))

    dwg.save()

def generate_expressions_map(topic, cat_data, output_path):
    prim, sec, acc = _colors("expressions")
    items = cat_data.get("items", [])
    dwg = svgwrite.Drawing(str(output_path), size=("800", "600"), profile="tiny")

    _add_gradient(dwg, "exp-bg", "#0d0d18", "#200e08")
    dwg.add(dwg.rect(insert=(0,0), size=("100%","100%"), rx=16, fill="url(#exp-bg)"))

    cx, cy = 400, 120
    label = cat_data.get("label", "")
    dwg.add(dwg.circle(center=(cx, cy), r=35, fill=prim, opacity=0.15))
    dwg.add(dwg.circle(center=(cx, cy), r=28, fill=prim, opacity=0.3))
    dwg.add(dwg.text(label, insert=(cx, cy+5), text_anchor="middle",
                      fill="#f1f5f9", font_size="16", font_weight="bold",
                      font_family="Inter, sans-serif"))

    for i, item in enumerate(items[:9]):
        col = i % 3
        row = i // 3
        x = 20 + col * 260
        y = 190 + row * 130

        card = dwg.add(dwg.rect(insert=(x, y), size=(250, 115), rx=10,
                                 fill="#0d0d18", stroke=prim, stroke_width=1, stroke_opacity=0.2))

        dwg.add(dwg.text(item.get("expression", ""), insert=(x+12, y+25), fill="#f1f5f9", font_size="14",
                          font_family="'Noto Sans JP', sans-serif"))
        dwg.add(dwg.text(item.get("reading", ""), insert=(x+12, y+48), fill="#64748b", font_size="10",
                          font_family="Inter, sans-serif"))
        dwg.add(dwg.text(item.get("meaning", ""), insert=(x+12, y+72), fill="#fb923c", font_size="11",
                          font_family="Inter, sans-serif"))
        dwg.add(dwg.text(item.get("usage", ""), insert=(x+12, y+100), fill="#475569", font_size="8",
                          font_family="Inter, sans-serif"))

    dwg.add(dwg.text(topic, insert=(400, 570), text_anchor="middle",
                      fill="#94a3b8", font_size="12", font_family="Inter, sans-serif"))
    dwg.save()

def generate_review_map(topic, review_type, all_data, output_path):
    dwg = svgwrite.Drawing(str(output_path), size=("800", "600"), profile="tiny")
    _add_gradient(dwg, "rev-bg", "#0d0d18", "#0a1820")
    dwg.add(dwg.rect(insert=(0,0), size=("100%","100%"), rx=16, fill="url(#rev-bg)"))

    dwg.add(dwg.circle(center=(400, 100), r=35, fill="#38bdf8", opacity=0.15))
    dwg.add(dwg.circle(center=(400, 100), r=28, fill="#38bdf8", opacity=0.3))
    dwg.add(dwg.text("Repaso", insert=(400, 105), text_anchor="middle",
                      fill="#f1f5f9", font_size="18", font_weight="bold",
                      font_family="Inter, sans-serif"))

    dwg.add(dwg.text(topic, insert=(400, 540), text_anchor="middle",
                      fill="#94a3b8", font_size="13", font_family="Inter, sans-serif"))
    dwg.save()

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
