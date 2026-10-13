@echo off
setlocal

:: Get date and time in YYYYMMDD_HHMMSS format
for /f %%I in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set "TIMESTAMP=%%I"

:: Set base backup dir and include timestamp folder
set "BASE_DIR=%USERPROFILE%\OneDrive - Ulster University\All Uni\Year 4\Semester 1\Full-stack Strategies and Development (COM661)\GitHub REPO\Uni\Year 4\Semester 1\COM661\MongoDB dumps"
set "BACKUP_DIR=%BASE_DIR%\%TIMESTAMP%"

echo Creating backup folder:
echo %BACKUP_DIR%
echo.
echo EXPORT: Starting MongoDB Export...
echo.

:: Run mongodump to export directly into timestamped folder
mongodump --gzip --out "%BACKUP_DIR%"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Export COMPLETED successfully.
	echo.
    echo Backup saved to:
    echo %BACKUP_DIR%
	echo.
) else (
    echo.
    echo Error: Export failed.
)
pause