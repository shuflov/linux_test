from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from PIL import Image
import io
import uvicorn

app = FastAPI()

ASCII_CHARS = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']

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

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        return {"error": "Only JPG and PNG files allowed"}
    
    contents = await file.read()
    ascii_art = convert_to_ascii(contents)
    return {"ascii": ascii_art}

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
