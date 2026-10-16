@echo off
REM Run the arena tournament (Windows CMD)
cd /d "%~dp0\.."
python -m pip install -r requirements.txt
python tools\arena.py --games 50 --k 16 %*
