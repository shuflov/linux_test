from fastapi import FastAPI, UploadFile, File, Request, Form
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from PIL import Image, ImageDraw, ImageFont
import io
import uvicorn

import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.mount("/static", StaticFiles(directory=BASE_DIR), name="static")

ASCII_CHARS = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']
FONT_SIZE = 12
CHAR_WIDTH = 7
CHAR_HEIGHT = 12

def resize_image(image, width=100):
    w, h = image.size
    ratio = h / w / 1.8
    new_height = int(width * ratio)
    return image.resize((width, new_height))

def convert_to_ascii(image_bytes, width=100):
    image = Image.open(io.BytesIO(image_bytes))
    image = resize_image(image, width)
    image = image.convert('L')
    pixels = image.getdata()
    chars = "".join([ASCII_CHARS[pixel // 25] for pixel in pixels])
    lines = [chars[i:i + width] for i in range(0, len(chars), width)]
    return "\n".join(lines)

def render_ascii_to_image(ascii_text, dark_mode=True, format="png"):
    lines = ascii_text.split('\n')
    width = len(lines[0]) if lines else 100
    height = len(lines)
    
    img_width = width * CHAR_WIDTH + 40
    img_height = height * CHAR_HEIGHT + 40
    
    bg_color = (13, 17, 23) if dark_mode else (255, 255, 255)
    text_color = (240, 246, 252) if dark_mode else (0, 0, 0)
    
    image = Image.new("RGB", (img_width, img_height), bg_color)
    draw = ImageDraw.Draw(image)
    
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", FONT_SIZE)
    except:
        font = ImageFont.load_default()
    
    for i, line in enumerate(lines):
        draw.text((20, 20 + i * CHAR_HEIGHT), line, fill=text_color, font=font)
    
    output = io.BytesIO()
    img_format = "PNG" if format == "png" else "JPEG"
    image.save(output, format=img_format)
    output.seek(0)
    return output.getvalue(), img_format.lower()

@app.post("/upload")
async def upload(file: UploadFile = File(...), width: int = 100):
    if file.content_type not in ["image/jpeg", "image/png"]:
        return {"error": "Only JPG and PNG files allowed"}
    
    contents = await file.read()
    ascii_art = convert_to_ascii(contents, width)
    return {"ascii": ascii_art}

@app.post("/download")
async def download(
    ascii_text: str = Form(...),
    format: str = Form("txt"),
    dark_mode: bool = Form(True)
):
    if format == "txt":
        return Response(
            content=ascii_text,
            media_type="text/plain",
            headers={"Content-Disposition": "attachment; filename=ascii_art.txt"}
        )
    
    if format == "html":
        bg_color = "#0d1117" if dark_mode else "#ffffff"
        text_color = "#f0f6fc" if dark_mode else "#000000"
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ASCII Art</title>
    <style>
        body {{
            background: {bg_color};
            color: {text_color};
            font-family: monospace;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }}
        pre {{
            font-size: 10px;
            line-height: 10px;
        }}
    </style>
</head>
<body>
<pre>
{ascii_text}
</pre>
</body>
</html>"""
        return Response(
            content=html_content,
            media_type="text/html",
            headers={"Content-Disposition": "attachment; filename=ascii_art.html"}
        )
    
    if format in ["png", "jpg", "jpeg"]:
        img_data, img_format = render_ascii_to_image(ascii_text, dark_mode, format)
        media_type = "image/png" if img_format == "png" else "image/jpeg"
        return Response(
            content=img_data,
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename=ascii_art.{img_format}"}
        )
    
    return {"error": "Unknown format"}

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/picture.png")
async def get_picture():
    picture_path = os.path.join(os.path.dirname(BASE_DIR), "picture.png")
    if os.path.exists(picture_path):
        with open(picture_path, "rb") as f:
            return Response(content=f.read(), media_type="image/png")
    return Response(status_code=404)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
