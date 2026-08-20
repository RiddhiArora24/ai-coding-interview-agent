from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


ROOT = Path(__file__).resolve().parents[1]

FRONTEND_DIST = (
    ROOT
    / "frontend"
    / "dist"
)


def mount_frontend(app: FastAPI):
    """
    Serve the React production build without using a
    catch-all route, so /api/* and /docs can never be
    intercepted by the frontend.
    """

    if not FRONTEND_DIST.exists():

        print(
            "frontend/dist not found; "
            "frontend static serving skipped."
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
            FRONTEND_DIST
            / "index.html"
        )