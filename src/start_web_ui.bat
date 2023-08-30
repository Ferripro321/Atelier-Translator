@echo off

if not exist env (
    echo Creating virtual environment...
    python3 -m venv env
) else (
    echo Virtual environment already exists. Skipping creation...
)

CALL .\env\Scripts\activate.bat

if exist requirements.txt (
    echo Installing dependencies from requirements.txt...
    pip install -r requirements.txt
) else (
    echo Error: requirements.txt not found!
    exit /b
)

python UI.py