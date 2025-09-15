@echo off
title Pariksha Header Generator
echo.
echo ========================================
echo   Pariksha Header Generator
echo ========================================
echo.
echo This tool helps you create professional headers
echo for your question papers.
echo.
echo Choose an option:
echo 1. Interactive Header Creator
echo 2. Quick Standard Header
echo 3. Quick University Header
echo 4. Quick Board Exam Header
echo 5. Exit
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto interactive
if "%choice%"=="2" goto standard
if "%choice%"=="3" goto university
if "%choice%"=="4" goto board
if "%choice%"=="5" goto exit

echo Invalid choice. Please try again.
pause
goto start

:interactive
echo.
echo Starting Interactive Header Creator...
cd /d "%~dp0"
python header.py --interactive
pause
goto start

:standard
echo.
echo Creating Standard School Header...
cd /d "%~dp0"
python header.py --template standard
pause
goto start

:university
echo.
echo Creating University Header...
cd /d "%~dp0"
python header.py --template university
pause
goto start

:board
echo.
echo Creating Board Exam Header...
cd /d "%~dp0"
python header.py --template board
pause
goto start

:exit
echo.
echo Thank you for using Pariksha Header Generator!
pause
exit