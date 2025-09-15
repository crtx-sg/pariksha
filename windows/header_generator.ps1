# Pariksha Header Generator PowerShell Script
# This script provides a menu-driven interface for creating question paper headers

param(
    [string]$Template = "",
    [switch]$Interactive = $false
)

function Show-Menu {
    Clear-Host
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "   Pariksha Header Generator" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "This tool helps you create professional headers" -ForegroundColor White
    Write-Host "for your question papers." -ForegroundColor White
    Write-Host ""
    Write-Host "Choose an option:" -ForegroundColor Green
    Write-Host "1. Interactive Header Creator" -ForegroundColor White
    Write-Host "2. Quick Standard Header" -ForegroundColor White
    Write-Host "3. Quick University Header" -ForegroundColor White
    Write-Host "4. Quick Board Exam Header" -ForegroundColor White
    Write-Host "5. Exit" -ForegroundColor White
    Write-Host ""
}

function Run-HeaderGenerator {
    param(
        [string]$Mode
    )

    $scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
    $headerScript = Join-Path $scriptPath "header.py"

    if (-not (Test-Path $headerScript)) {
        $headerScript = "header.py"
    }

    try {
        switch ($Mode) {
            "interactive" {
                Write-Host "Starting Interactive Header Creator..." -ForegroundColor Green
                python $headerScript --interactive
            }
            "standard" {
                Write-Host "Creating Standard School Header..." -ForegroundColor Green
                python $headerScript --template standard
            }
            "university" {
                Write-Host "Creating University Header..." -ForegroundColor Green
                python $headerScript --template university
            }
            "board" {
                Write-Host "Creating Board Exam Header..." -ForegroundColor Green
                python $headerScript --template board
            }
        }
        Write-Host ""
        Write-Host "Header generation completed!" -ForegroundColor Green
    } catch {
        Write-Host "Error running header generator: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "Make sure Python is installed and in your PATH." -ForegroundColor Yellow
    }

    Write-Host ""
    Write-Host "Press any key to continue..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

# Main execution logic
if ($Interactive) {
    Run-HeaderGenerator -Mode "interactive"
    exit
}

if ($Template -ne "") {
    Run-HeaderGenerator -Mode $Template
    exit
}

# Interactive menu mode
do {
    Show-Menu
    $choice = Read-Host "Enter your choice (1-5)"

    switch ($choice) {
        "1" { Run-HeaderGenerator -Mode "interactive" }
        "2" { Run-HeaderGenerator -Mode "standard" }
        "3" { Run-HeaderGenerator -Mode "university" }
        "4" { Run-HeaderGenerator -Mode "board" }
        "5" {
            Write-Host ""
            Write-Host "Thank you for using Pariksha Header Generator!" -ForegroundColor Green
            exit
        }
        default {
            Write-Host ""
            Write-Host "Invalid choice. Please try again." -ForegroundColor Red
            Start-Sleep -Seconds 2
        }
    }
} while ($true)