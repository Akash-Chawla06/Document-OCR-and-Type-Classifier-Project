import re
import shutil
from os import path

import pytesseract
from fastapi import APIRouter, File, HTTPException, Request, UploadFile, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pytesseract.pytesseract import TesseractError
# Instantiate OCR router
ocr_router = APIRouter(tags=["OCR"])

# Get absolute path of '/static' folder
ASSETS_DIR = path.abspath("static")

# Define template
templates = Jinja2Templates(directory="templates")
@ocr_router.post('/ocr', response_class=HTMLResponse)
def ocr(request: Request, image: UploadFile = File(...)):

    file_path = path.join(ASSETS_DIR, image.filename)
    api_path = f"/static/{image.filename}"

    with open(file_path, "w+b") as buffer:
        # Copy file to static folder
        if re.search(pattern="(?:jpg|jpeg|png|bmp)", string=image.filename) is not None:
            shutil.copyfileobj(image.file, buffer)
        
        #  Translate to text
        try:
            text = pytesseract.image_to_string(file_path, lang='eng')

        except TesseractError:
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    return templates.TemplateResponse("home.html", {"request": request, "message": "File uploaded successfully",
                                                    "text": text,
                                                    "image_path": api_path}, status_code=200)