import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil, uuid
from scoring.engine import evaluate_resume_for_jd

app = FastAPI()
STORAGE = Path("storage")
STORAGE.mkdir(exist_ok=True)

@app.post("/evaluate/")
async def evaluate(jd_path: str = Form(...), resume_path: str = Form(...)):
    try:
        result = evaluate_resume_for_jd(jd_path, resume_path)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
