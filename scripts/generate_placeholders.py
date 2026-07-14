import svgwrite
import random
from pathlib import Path

ANIME_DIR = Path(__file__).resolve().parent.parent / "data" / "anime"
ANIME_DIR.mkdir(parents=True, exist_ok=True)

def _hex():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

PALETTES = [
    ("#1a0a2e", "#16213e", "#0f3460", "#e94560"),
    ("#0d1b2a", "#1b2838", "#415a77", "#778da9"),
    ("#1a1a2e", "#16213e", "#0f3460", "#533483"),
    ("#0f0c29", "#302b63", "#24243e", "#e94560"),
    ("#000428", "#004e92", "#00b4db", "#0083b0"),
]

def generate_placeholder(idx):
    pal = random.choice(PALETTES)
    dwg = svgwrite.Drawing(str(ANIME_DIR / f"bg-{idx:02d}.svg"), size=("1920", "1080"))

    grad = dwg.defs.add(dwg.linearGradient(id=f"bg{idx}", x1="0%", y1="0%", x2="100%", y2="100%"))
    grad.add_stop_color("0%", pal[0])
    grad.add_stop_color("50%", pal[1])
    grad.add_stop_color("100%", pal[2])

    dwg.add(dwg.rect(insert=(0,0), size=("100%","100%"), fill=f"url(#bg{idx})"))

    for _ in range(random.randint(3, 8)):
        cx = random.randint(100, 1800)
        cy = random.randint(100, 900)
        r = random.randint(50, 300)
        opacity = random.uniform(0.03, 0.08)
        color = random.choice(pal[1:])
        dwg.add(dwg.circle(center=(cx, cy), r=r, fill=color, opacity=opacity))

    for _ in range(random.randint(2, 5)):
        x = random.randint(50, 1850)
        y = random.randint(50, 1000)
        angle = random.randint(-30, 30)
        lines = random.randint(3, 8)
        spacing = random.randint(8, 20)
        opacity = random.uniform(0.02, 0.05)
        group = dwg.add(dwg.g(opacity=opacity))
        for i in range(lines):
            group.add(dwg.line(start=(x + i * spacing, y), end=(x + i * spacing + 100, y - 300),
                               stroke=pal[3], stroke_width=1))

    dwg.add(dwg.rect(insert=(0,0), size=("100%","100%"), fill="#000000", opacity=0.15))

    dwg.save()

def main():
    for i in range(1, 31):
        path = ANIME_DIR / f"bg-{i:02d}.svg"
        if not path.exists():
            generate_placeholder(i)
            print(f"  Generado bg-{i:02d}.svg")
        else:
            print(f"  bg-{i:02d}.svg ya existe")
    print(f"\n✓ Placeholders generados en {ANIME_DIR}")

if __name__ == "__main__":
    main()
