from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

def create_app(config: dict) -> FastAPI:
    app = FastAPI(title="Niji Mindmaps")
    output_dir = Path(config.get("storage", {}).get("output_dir", "docs"))
    output_dir.mkdir(parents=True, exist_ok=True)

    @app.get("/")
    def index():
        return FileResponse(output_dir / "index.html")

    @app.get("/{path:path}")
    def static(path: str):
        fp = output_dir / path
        if fp.exists() and fp.is_file():
            return FileResponse(fp)
        return FileResponse(output_dir / "index.html")

    return app

def start_server(config: dict):
    import uvicorn
    host = config.get("server", {}).get("host", "0.0.0.0")
    port = config.get("server", {}).get("port", 8000)
    app = create_app(config)
    uvicorn.run(app, host=host, port=port)
