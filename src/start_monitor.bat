@echo off
REM Launch script for Ricn Mall Product Monitor

cd /d "%~dp0"
echo Starting Ricn Mall Product Monitor...
python product_monitor.py --config ../config.json
if errorlevel 1 (
    echo An error occurred while running the product monitor.
    pause
)