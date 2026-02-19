# ASCII Art Converter

Upload any image (JPG/PNG) and convert it to ASCII art.

## Quick Start

```bash
pip install -r requirements.txt
python3 app.py
```

Then open http://localhost:8080

## Features

- Upload JPG or PNG images
- Adjustable ASCII width (50-150 characters)
- Dark terminal theme
- Copy ASCII result

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web interface |
| POST | `/upload` | Convert image to ASCII |

### Upload Example

```bash
curl -X POST -F "file=@image.jpg" -F "width=100" http://localhost:8080/upload
```

## Running

```bash
python3 app.py
```

Server runs on http://localhost:8080
