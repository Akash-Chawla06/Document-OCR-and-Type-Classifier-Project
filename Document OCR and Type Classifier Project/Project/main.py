import os

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from router import ocr_router
# Instantiate an App
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Include OCR router to the app
app.include_router(ocr_router)

# Create a static folder for image display
upload_dir = "static"
if not os.path.exists(upload_dir):
    os.mkdir(upload_dir)

# Mount '/static' folder into the app
app.mount("/static", StaticFiles(directory=upload_dir), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})