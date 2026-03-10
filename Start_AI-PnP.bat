@echo off
setlocal
cd /d "%~dp0"

where pyw >nul 2>nul
if not errorlevel 1 (
    start "" pyw -3 main.py
    goto :eof
)

where pythonw >nul 2>nul
if not errorlevel 1 (
    start "" pythonw main.py
    goto :eof
)

where py >nul 2>nul
if not errorlevel 1 (
    start "" py -3 main.py
    goto :eof
)

where python >nul 2>nul
if not errorlevel 1 (
    start "" python main.py
    goto :eof
)

echo Python 3.11+ wurde nicht gefunden.
echo Bitte Python installieren oder den Python-Launcher aktivieren.
pause
