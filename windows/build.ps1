# PowerShell script to build Windows application
# Run this with: powershell -ExecutionPolicy Bypass -File build.ps1

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "    Building Pariksha for Windows" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "🚀 Starting build process..." -ForegroundColor Green
Write-Host "This will create a standalone Windows application." -ForegroundColor Yellow
Write-Host "Please wait while the build completes (may take several minutes)..." -ForegroundColor Yellow
Write-Host ""

try {
    # Run the build script
    python build_windows_app.py

    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Build completed successfully!" -ForegroundColor Green
        Write-Host "📦 Check the 'Pariksha_Windows_App' folder for the application." -ForegroundColor Cyan
        Write-Host ""
        Write-Host "📋 Next steps:" -ForegroundColor Yellow
        Write-Host "1. Test the app by running Start_Pariksha.bat" -ForegroundColor White
        Write-Host "2. Zip the Pariksha_Windows_App folder for distribution" -ForegroundColor White
        Write-Host "3. Share with end users" -ForegroundColor White
    } else {
        Write-Host "❌ Build failed! Check the error messages above." -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Error during build: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")