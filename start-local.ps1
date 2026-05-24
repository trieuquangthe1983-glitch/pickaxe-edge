# Launch pickaxe-edge locally on port 8503 (avoids audience-edge on 8501).
# Usage:  ./start-local.ps1
#
# This is the local dev shortcut. Streamlit Cloud / Render / Fly use their own
# entry points and ignore this script.

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

streamlit run ui/app.py `
    --server.port=8503 `
    --server.headless=true `
    --browser.gatherUsageStats=false
