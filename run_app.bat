@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    py -3.11 -m venv .venv
)
call .venv\Scripts\activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
start "Backend" cmd /k "call .venv\Scripts\activate && python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000"
timeout /t 1 >nul
start "Frontend" cmd /k "call .venv\Scripts\activate && streamlit run frontend/streamlit_app.py"
exit /b 0
