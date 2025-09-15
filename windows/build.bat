@echo off
title Building Teacher Question Paper System for Windows
echo.
echo ============================================================
echo    Building Teacher Question Paper System for Windows
echo ============================================================
echo.
echo This will create a standalone Windows application that
echo includes Python and all required libraries.
echo.
echo Please wait while the build process completes...
echo This may take several minutes.
echo.
pause

python build_windows_app.py

echo.
echo ============================================================
echo Build process completed!
echo Check the Windows_App_Distribution folder for the result.
echo ============================================================
pause