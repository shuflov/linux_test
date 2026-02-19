from http.server import HTTPServer, BaseHTTPRequestHandler
from PIL import Image
import ascii

ASCII_CHARS = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']

def image_to_ascii_str(image_path, width=100):
    image = Image.open(image_path)
    width, height = image.size
    ratio = height / width / 1.8
    new_height = int(width * ratio)
    image = image.resize((width, new_height))
    image = image.convert('L')
    pixels = image.getdata()
    characters = "".join([ASCII_CHARS[pixel // 25] for pixel in pixels])
    lines = [characters[i:i + width] for i in range(0, len(characters), width)]
    return "\n".join(lines)

ascii_art = image_to_ascii_str('picture.png')

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASCII Art</title>
    <style>
        body {{
            background: #0d1117;
            color: #f0f6fc;
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
{ascii_art}
</pre>
</body>
</html>"""

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/cat':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(ascii_art.encode())
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode())

print("Server running on http://localhost:8080")
print("curl -s localhost:8080/cat")
HTTPServer(('0.0.0.0', 8080), Handler).serve_forever()
