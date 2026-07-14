import json
import shutil
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

class SiteBuilder:
    def __init__(self, config: dict):
        self.config = config
        template_dir = Path(__file__).parent / "templates"
        self.env = Environment(loader=FileSystemLoader(str(template_dir)))

    def build(self, output_dir: Path, mindmaps: list[dict]):
        output_dir.mkdir(parents=True, exist_ok=True)
        assets_dir = output_dir / "assets"
        assets_dir.mkdir(exist_ok=True)
        mindmaps_dir = output_dir / "mindmaps"
        mindmaps_dir.mkdir(exist_ok=True)
        archive_dir = output_dir / "archive"
        archive_dir.mkdir(exist_ok=True)

        self._write_assets(assets_dir)
        self._copy_anime(output_dir)

        today = datetime.now().strftime("%Y-%m-%d")
        today_map = next((m for m in mindmaps if m.get("date") == today), None)
        recent = sorted(mindmaps, key=lambda x: x.get("date", ""), reverse=True)[:12]

        total_categories = set(m.get("category", "review") for m in mindmaps)

        self._render("index.html", output_dir / "index.html", {
            "today_map": today_map,
            "recent_maps": recent,
            "total_maps": len(mindmaps),
            "total_days": len(set(m.get("date", "") for m in mindmaps)),
            "categories": list(total_categories),
            "calendar": mindmaps[-30:],
            "root_path": "",
            "css_path": "assets/",
        })

        for mm in mindmaps:
            mm_dir = output_dir / "mindmap"
            mm_dir.mkdir(exist_ok=True)

            self._render("mindmap.html", mm_dir / f"{mm['id']}.html", {
                "mmap": mm,
                "root_path": "../",
                "css_path": "../assets/",
            })

        self._generate_archive(output_dir, mindmaps)
        self._generate_search_index(output_dir, mindmaps)

    def _generate_archive(self, output_dir, mindmaps):
        dates = sorted(set(m.get("date", "") for m in mindmaps if m.get("date")), reverse=True)
        years = defaultdict(lambda: defaultdict(lambda: {"label": "", "count": 0, "days": 0}))

        for d in dates:
            year = d[:4]
            month_key = d[:7]
            dt = datetime.strptime(month_key + "-01", "%Y-%m-%d")
            years[year][month_key]["label"] = dt.strftime("%B")
            years[year][month_key]["count"] += 1
            years[year][month_key]["days"] = len(set(
                dd for dd in dates if dd.startswith(month_key)
            ))

        self._render("archive.html", output_dir / "archive.html", {
            "archive": dict(years),
            "root_path": "",
            "css_path": "assets/",
        })

        for year, months in years.items():
            for month_key, month_data in months.items():
                month_maps = [m for m in mindmaps if m.get("date", "").startswith(month_key)]
                self._render("archive.html", output_dir / "archive" / f"{month_key}.html", {
                    "archive": {year: {month_key: month_data}},
                    "mindmaps": month_maps,
                    "root_path": "../",
                    "css_path": "../assets/",
                })

    def _generate_search_index(self, output_dir, mindmaps):
        index = []
        for m in mindmaps:
            index.append({
                "id": m.get("id", ""),
                "title": m.get("title", ""),
                "description": (m.get("description", "") or "")[:200],
                "category": m.get("category", ""),
                "date": m.get("date", ""),
                "tags": m.get("tags", []),
                "svg_path": m.get("svg_path", ""),
            })
        with open(output_dir / "mindmaps" / "index.json", "w", encoding="utf-8") as f:
            json.dump(index, f, ensure_ascii=False)

    def _copy_anime(self, output_dir):
        anime_dir = self.config.get("storage", {}).get("anime_dir", "data/anime")
        src = Path(anime_dir)
        if src.exists():
            dst = output_dir / "assets" / "anime"
            dst.mkdir(exist_ok=True)
            for f in src.glob("*"):
                if f.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp"):
                    shutil.copy2(f, dst / f.name)

    def _render(self, template_name: str, output_path: Path, context: dict):
        template = self.env.get_template(template_name)
        html = template.render(**context)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

    def _write_assets(self, assets_dir: Path):
        css_src = Path(__file__).parent.parent / "src" / "style.css"
        if css_src.exists():
            shutil.copy2(css_src, assets_dir / "style.css")
        else:
            css = open(Path(__file__).parent.parent / "style.css").read()
            with open(assets_dir / "style.css", "w") as f:
                f.write(css)

        js = """(function(){
var s = document.querySelector('script[src$="app.js"]');
var base = s ? s.src.substring(0, s.src.lastIndexOf('/')) + '/' : '';
var bgDir = base + 'anime/';

function setBg() {
  var exts = ['jpg','jpeg','png','webp','svg'];
  var pool = [];
  for (var i = 1; i <= 30; i++) {
    var num = ('0' + i).slice(-2);
    exts.forEach(function(ext) { pool.push(bgDir + 'bg-' + num + '.' + ext); });
  }
  var pick = pool[Math.floor(Math.random() * pool.length)];
  var img = new Image();
  img.onload = function() { document.body.style.backgroundImage = 'url(' + pick + ')'; };
  img.src = pick;
}
setBg();

document.addEventListener('DOMContentLoaded', function() {
  var cards = document.querySelectorAll('.glass-card');
  if ('IntersectionObserver' in window) {
    var obs = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          entry.target.style.animationPlayState = 'running';
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });
    cards.forEach(function(c) { c.style.animationPlayState = 'paused'; obs.observe(c); });
  }

  var cur = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav a:not(.nav-brand)').forEach(function(a) {
    if (a.getAttribute('href') === cur) a.classList.add('active');
  });
});
})();
"""
        with open(assets_dir / "app.js", "w") as f:
            f.write(js)
