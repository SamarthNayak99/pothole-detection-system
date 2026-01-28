# Quick Start Script for Railway Deployment
# Run this in PowerShell to get started

Write-Host "Pothole Detection App - Railway Deployment Setup" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Git is installed
Write-Host "Checking prerequisites..." -ForegroundColor Yellow
try {
    $gitVersion = git --version
    Write-Host "[OK] Git is installed: $gitVersion" -ForegroundColor Green
}
catch {
    Write-Host "[ERROR] Git is NOT installed!" -ForegroundColor Red
    Write-Host "   Please download from: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "1. Configure Git (if first time):" -ForegroundColor White
Write-Host "   git config --global user.name 'Your Name'" -ForegroundColor Gray
Write-Host "   git config --global user.email 'your-email@example.com'" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Initialize Git repository:" -ForegroundColor White
Write-Host "   git init" -ForegroundColor Gray
Write-Host "   git add ." -ForegroundColor Gray
Write-Host "   git commit -m 'Initial commit - Pothole Detection App'" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Create GitHub repository:" -ForegroundColor White
Write-Host "   Go to: https://github.com/new" -ForegroundColor Gray
Write-Host "   Name: pothole-detection-app" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Push to GitHub:" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/YOUR-USERNAME/pothole-detection-app.git" -ForegroundColor Gray
Write-Host "   git branch -M main" -ForegroundColor Gray
Write-Host "   git push -u origin main" -ForegroundColor Gray
Write-Host ""
Write-Host "5. Deploy on Railway:" -ForegroundColor White
Write-Host "   Go to: https://railway.app" -ForegroundColor Gray
Write-Host "   Sign in with GitHub" -ForegroundColor Gray
Write-Host "   Create new project from your GitHub repo" -ForegroundColor Gray
Write-Host ""
Write-Host "For detailed instructions, see: RAILWAY_DEPLOYMENT_GUIDE.md" -ForegroundColor Cyan
Write-Host ""
Write-Host "IMPORTANT: Add these environment variables in Railway:" -ForegroundColor Yellow
Write-Host "   EMAIL_SENDER=rvcedtl@gmail.com" -ForegroundColor Gray
Write-Host "   EMAIL_PASSWORD=vznt ndxz ktmo orqf" -ForegroundColor Gray
Write-Host "   EMAIL_RECEIVER=samnayak64@gmail.com" -ForegroundColor Gray
Write-Host "   PORT=8000" -ForegroundColor Gray
Write-Host ""
Write-Host "Ready to deploy! Good luck!" -ForegroundColor Green
