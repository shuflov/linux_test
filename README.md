# ASCII Art Converter

Upload any image (JPG/PNG) and convert it to ASCII art.

## For Users (Online - No Installation)

**Live at:** https://shuflov.github.io/ascii_converter/

Simply open the link above in your browser, upload an image, and download in TXT, HTML, PNG, or JPG format.

## For Developers (Local Development)

This project has two parts:

```
docs/           → GitHub Pages (client-side JavaScript, no server needed)
server/         → Python backend (requires Python server)
```

### Option 1: GitHub Pages (Online)

The `docs/` folder contains a fully client-side version that runs in the browser without any server.

1. **Use live:** https://shuflov.github.io/ascii_converter/

2. **Run locally:** Just open `docs/index.html` in any browser

### Option 2: Python Backend (Full Control)

The `server/` folder contains a Python FastAPI server for local development.

#### Setup

```bash
cd server
pip install -r requirements.txt
python3 app.py
```

Then open http://localhost:8080

#### Features

- Upload JPG or PNG images
- Adjustable ASCII width (50-150 characters)
- Dark/Light background
- Download as TXT, HTML, PNG, or JPG

#### API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web interface |
| POST | `/upload` | Convert image to ASCII |
| POST | `/download` | Download in specified format |

#### Upload Example

```bash
curl -X POST -F "file=@image.jpg" -F "width=100" http://localhost:8080/upload
```

## Files

```
docs/index.html          → GitHub Pages version (client-side JS)
server/app.py            → Python FastAPI backend
server/requirements.txt  → Python dependencies
server/templates/        → Backend HTML templates
picture.png             → Sample image for testing
```

## Contributing

This code is free and open source. Feel free to fork, modify, and use as you like.

## License

MIT License - Use freely for any purpose.
