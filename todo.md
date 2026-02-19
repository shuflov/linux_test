# ASCII Art Converter - Project Todo

## Tech Stack
- **Backend:** FastAPI (Python)
- **Frontend:** HTML + JavaScript
- **Deployment:** Your own server

## Steps

### Step 1: Setup
- [x] Install FastAPI and Uvicorn
- [x] Create `requirements.txt`
- [x] Create basic FastAPI app structure

### Step 2: Backend - Core Logic
- [x] Create ASCII conversion function
- [x] Create `/upload` POST endpoint
- [x] Add file validation (.jpg, .png)
- [x] Return ASCII as JSON response

### Step 3: Backend - Static Files
- [ ] Configure static files serving
- [ ] Create `index.html` with upload form

### Step 4: Frontend - Upload UI
- [ ] Dark terminal-themed HTML
- [ ] File upload input
- [ ] Width/size slider

### Step 5: Frontend - JavaScript
- [ ] Handle form submit
- [ ] Send image to `/upload`
- [ ] Display ASCII result

### Step 6: Refinement
- [ ] Add copy to clipboard
- [ ] Error handling
- [ ] Test and verify

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Serve upload page |
| POST | `/upload` | Convert image to ASCII |
| GET | `/static/*` | Serve static files |

## Running the Server

```bash
uvicorn app:app --reload --port 8080
```

Then open `http://localhost:8080`
