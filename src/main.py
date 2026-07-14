import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import argparse
import yaml
from datetime import datetime, timedelta
from rich.console import Console

from src.generator import generate
from src.ai_enhancer import AIEnhancer
from src.builder import SiteBuilder

console = Console()

def load_config(path="config.yaml"):
    with open(path) as f:
        return yaml.safe_load(f)

def load_content(base_dir, filename):
    path = Path(base_dir) / filename
    if path.exists():
        with open(path) as f:
            return yaml.safe_load(f)
    return {}

def daily(config):
    today = datetime.now()
    base_dir = config.get("storage", {}).get("content_dir", "data/content")
    schedule_path = config.get("storage", {}).get("schedule_file", "data/schedule.yaml")
    output_dir = Path(config.get("storage", {}).get("output_dir", "docs"))

    with open(schedule_path) as f:
        schedule = yaml.safe_load(f)["rotation"]

    cutoff = datetime(2026, 7, 14)
    day_index = (today - cutoff).days
    if day_index < 0:
        day_index = 0

    schedule_entry = schedule[day_index % len(schedule)]
    category = schedule_entry["category"]
    topic_id = schedule_entry["topic_id"]
    title = schedule_entry["title"]

    console.print(f"[bold cyan]Niji Mindmaps — {today.strftime('%Y-%m-%d')}[/bold cyan]")
    console.print(f"Tema: [bold]{title}[/bold] ({category})")

    content = load_content(base_dir, f"{category}.yaml")
    if not content:
        console.print(f"[red]No content file found for category: {category}[/red]")
        return

    enhancer = AIEnhancer(config)

    topic_data = None
    if category in ("hiragana", "katakana"):
        for row in content.get("rows", []):
            if row.get("id") == topic_id:
                topic_data = row
                break
    elif category in ("kanji", "vocabulary"):
        for theme in content.get("themes", []):
            if theme.get("id") == topic_id:
                topic_data = theme
                break
    elif category == "grammar":
        for topic in content.get("topics", []):
            if topic.get("id") == topic_id:
                topic_data = topic
                break
    elif category == "expressions":
        for cat in content.get("categories", []):
            if cat.get("id") == topic_id:
                topic_data = cat
                break
    elif category == "review":
        topic_data = {"type": topic_id, "data": content}

    if not topic_data:
        console.print(f"[red]Topic '{topic_id}' not found in {category}.yaml[/red]")
        return

    enhance_fn = getattr(enhancer, f"enhance_{category}", None)
    if enhance_fn:
        enhanced = enhance_fn(topic_data)
        if enhanced:
            topic_data = enhanced

    maps_dir = output_dir / "mindmaps"
    maps_dir.mkdir(parents=True, exist_ok=True)

    date_str = today.strftime("%Y-%m-%d")
    map_id = f"{date_str}-{category}-{topic_id}"
    svg_filename = f"{map_id}.svg"
    svg_path = maps_dir / svg_filename

    generate(category, title, topic_data, svg_path)

    mindmap_entry = {
        "id": map_id,
        "title": title,
        "category": category,
        "date": date_str,
        "svg_path": svg_filename,
        "description": f"Mapa mental diario: {title}",
        "tags": [category, topic_id],
    }

    console.print(f"[green]✓ SVG generado: {svg_filename}[/green]")
    return mindmap_entry

def load_existing_mindmaps(output_dir):
    index_path = output_dir / "mindmaps" / "index.json"
    if index_path.exists():
        import json
        with open(index_path) as f:
            return json.load(f)
    return []

def build(config):
    output_dir = Path(config.get("storage", {}).get("output_dir", "docs"))
    builder = SiteBuilder(config)
    existing = load_existing_mindmaps(output_dir)
    new_map = daily(config)

    all_maps = existing
    if new_map:
        existing_ids = {m.get("id") for m in all_maps}
        if new_map["id"] not in existing_ids:
            all_maps.insert(0, new_map)

    if not all_maps:
        all_maps = [new_map] if new_map else []

    builder.build(output_dir, all_maps)
    console.print(f"[bold green]✓ Sitio generado en {output_dir}/[/bold green]")

def serve(config):
    from src.server import start_server
    start_server(config)

def main():
    parser = argparse.ArgumentParser(description="Niji Mindmaps — Mapas mentales diarios para japonés")
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--daily", action="store_true", help="Generar mapa del día")
    parser.add_argument("--build", action="store_true", help="Generar mapa + sitio completo")
    parser.add_argument("--serve", action="store_true", help="Iniciar servidor web")
    args = parser.parse_args()

    config = load_config(args.config)

    if args.daily:
        daily(config)
    elif args.build:
        build(config)
    elif args.serve:
        serve(config)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
