from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles


ROOT = Path(__file__).resolve().parents[1]
FRONTEND_DIST = ROOT / "frontend" / "dist"


def mount_frontend(app: FastAPI):

    if not FRONTEND_DIST.exists():
        print(
            "frontend/dist not found; "
            "production frontend serving skipped."
        )
        return

    assets = FRONTEND_DIST / "assets"

    if assets.exists():
        app.mount(
            "/assets",
            StaticFiles(
                directory=str(assets)
            ),
            name="frontend-assets"
        )

    @app.get(
        "/",
        include_in_schema=False
    )
    async def frontend_root():
        return FileResponse(
            FRONTEND_DIST / "index.html"
        )

    @app.get(
        "/{full_path:path}",
        include_in_schema=False
    )
    async def frontend_fallback(
        full_path: str
    ):

        if full_path.startswith("api/"):
            return JSONResponse(
                status_code=404,
                content={
                    "detail": "Not Found"
                }
            )

        root = FRONTEND_DIST.resolve()
        candidate = (
            FRONTEND_DIST / full_path
        ).resolve()

        try:
            candidate.relative_to(root)

        except ValueError:
            return JSONResponse(
                status_code=404,
                content={
                    "detail": "Not Found"
                }
            )

        if candidate.is_file():
            return FileResponse(candidate)

        return FileResponse(
            FRONTEND_DIST / "index.html"
        )
