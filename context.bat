@echo off
setlocal enabledelayedexpansion

REM === Define output file (same folder as this script) ===
set "OUTPUT_FILE=%~dp0project_context.txt"

REM === Clean start ===
if exist "%OUTPUT_FILE%" del "%OUTPUT_FILE%"

echo ###################################### >> "%OUTPUT_FILE%"
echo # PORTFOLIO PROJECT CONTEXT FILE # >> "%OUTPUT_FILE%"
echo ###################################### >> "%OUTPUT_FILE%"
echo. >> "%OUTPUT_FILE%"

echo --- USING GIT-TRACKED FILES ONLY --- >> "%OUTPUT_FILE%"
echo. >> "%OUTPUT_FILE%"

REM === Repo structure ===
echo --- REPOSITORY STRUCTURE --- >> "%OUTPUT_FILE%"
dir /b /ad >> "%OUTPUT_FILE%"
echo. >> "%OUTPUT_FILE%"

REM === List tracked files ===
echo --- INCLUDED FILES (tracked by Git) --- >> "%OUTPUT_FILE%"
git ls-files > "%TEMP%\gitfiles.txt"

for /f "usebackq delims=" %%F in ("%TEMP%\gitfiles.txt") do (
    echo %%F >> "%OUTPUT_FILE%"
)
echo. >> "%OUTPUT_FILE%"

REM === Append each file’s contents ===
for /f "usebackq delims=" %%F in ("%TEMP%\gitfiles.txt") do (
    set "FILE=%%F"
    echo ====================================== >> "%OUTPUT_FILE%"
    echo === FILE: !FILE! === >> "%OUTPUT_FILE%"
    echo ====================================== >> "%OUTPUT_FILE%"
    if exist "!FILE!" (
        type "!FILE!" >> "%OUTPUT_FILE%"
    ) else (
        echo [WARNING] File not found: !FILE! >> "%OUTPUT_FILE%"
    )
    echo. >> "%OUTPUT_FILE%"
)

echo DONE - Output written to "%OUTPUT_FILE%"
pause
