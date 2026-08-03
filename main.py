import uuid
from pathlib import Path

from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from utils import run_detection

app = FastAPI(title="DetectronV8")

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
MEDIA_DIR = BASE_DIR / "media"
UPLOADS_DIR = MEDIA_DIR / "uploads"
PROCESSED_DIR = MEDIA_DIR / "processed"

STATIC_DIR.mkdir(parents=True, exist_ok=True)
MEDIA_DIR.mkdir(parents=True, exist_ok=True)
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.mount("/media", StaticFiles(directory=str(MEDIA_DIR)), name="media")

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"request": request},
    )


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="about.html",
        context={"request": request},
    )


@app.get("/detect", response_class=HTMLResponse)
async def detect_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="detection.html",
        context={
            "request": request,
            "image_url": None,
            "detections": [],
        },
    )


@app.post("/detect", response_class=HTMLResponse)
async def detect_submit(request: Request, image: UploadFile = File(...)):
    ext = Path(image.filename).suffix or ".jpg"
    unique_name = f"{uuid.uuid4().hex}{ext}"
    upload_path = UPLOADS_DIR / unique_name
    upload_path.write_bytes(await image.read())

    processed_image_path, raw_detections = run_detection(
        str(upload_path),
        str(PROCESSED_DIR),
    )

    detections = []
    for item in (raw_detections or []):
        conf = float(item.get("confidence", 0))
        detections.append(
            {
                "label": item.get("label", "unknown"),
                "confidence": f"{round(conf * 100, 1)}%",
            }
        )

    image_url = f"/media/processed/{Path(processed_image_path).name}"

    return templates.TemplateResponse(
        request=request,
        name="detection.html",
        context={
            "request": request,
            "image_url": image_url,
            "detections": detections,
        },
    )