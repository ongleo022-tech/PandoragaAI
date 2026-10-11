@echo off
title Pandoraga Omega - Chess Engine
cd /d "%~dp0"

echo ========================================
echo PANDORAGA OMEGA
echo ========================================
echo.

where py >nul 2>&1
if %errorlevel%==0 (
    py -3 Pandoraga.py
    goto end
)

where python >nul 2>&1
if %errorlevel%==0 (
    python Pandoraga.py
    goto end
)

echo ERREUR : Python 3 est introuvable.
echo Installe Python depuis https://www.python.org/downloads/
echo Puis relance ce fichier.
pause

:end
if not "%errorlevel%"=="0" pause
