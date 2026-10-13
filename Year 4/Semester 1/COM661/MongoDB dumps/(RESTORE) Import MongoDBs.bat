@echo off
setlocal EnableDelayedExpansion

:: Base directory containing MongoDB backup folders
set "BASE_DIR=%USERPROFILE%\OneDrive - Ulster University\All Uni\Year 4\Semester 1\Full-stack Strategies and Development (COM661)\GitHub REPO\Uni\Year 4\Semester 1\COM661\MongoDB dumps"

echo.
echo =========================================
echo ============ MongoDB Restore ============
echo =========================================
echo.
echo Looking for latest backup...
echo.

:: Check backup directory exists
if not exist "!BASE_DIR!" (
    echo ERROR: Backup directory not found:
    echo !BASE_DIR!
    goto end
)

:: Change to the backup directory - **START**
pushd "!BASE_DIR!"

:: Find newest backup folder
:: /AD = directories only
:: /O:D = sort by date, oldest to newest
:: /B = bare folder names
for /f "delims=" %%I in ('dir /AD /O:D /B') do set "LATEST_FOLDER=%%I"

:: Return to original directory - **END**
popd

:: Check whether backup was found
if not defined LATEST_FOLDER (
    echo ERROR: No backup folders found in:
    echo !BASE_DIR!
    goto end
)

:: Build full path to latest backup
set "FULL_RESTORE_PATH=!BASE_DIR!\!LATEST_FOLDER!"

echo Found latest backup:
echo !LATEST_FOLDER!
echo.
echo Restore path:
echo !FULL_RESTORE_PATH!
echo.

:: WARNING
echo WARNING: This will DROP existing MongoDB collections
echo before restoring the backup.
echo.
choice /C YN /M "Continue with restore"

if errorlevel 2 (
    echo.
    echo Restore cancelled.
    goto end
)

echo.
echo IMPORT: Starting MongoDB restore...
echo.

:: Restore the latest backup
mongorestore --drop --gzip "!FULL_RESTORE_PATH!"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ==========================================
    echo ===== RESTORE COMPLETED SUCCESSFULLY =====
    echo ==========================================
    echo.
    echo Restored from:
    echo !FULL_RESTORE_PATH!
) else (
    echo.
    echo =========================================
    echo ========= ERROR: Restore failed =========
    echo =========================================
)

:end
echo.
pause