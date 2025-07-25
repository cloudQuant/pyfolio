@echo off
REM Script to check CI/CD status using GitHub CLI
REM Requires GitHub CLI (gh) to be installed

echo === Checking CI/CD Status for pyfolio ===
echo.

REM Check if gh is installed
gh --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: GitHub CLI is not installed.
    echo Please install it from: https://cli.github.com/
    exit /b 1
)

REM Get repository info
for /f "tokens=*" %%i in ('git remote get-url origin') do set REPO_URL=%%i
echo Repository: %REPO_URL%
echo.

REM Extract owner/repo from URL
REM This works for both https and ssh URLs
set REPO=%REPO_URL%
set REPO=%REPO:https://github.com/=%
set REPO=%REPO:git@github.com:=%
set REPO=%REPO:.git=%
set REPO=cloudQuant/pyfolio

echo Checking workflows for: %REPO%
echo.

REM List recent workflow runs
echo === Recent Workflow Runs ===
gh run list --repo %REPO% --limit 10

echo.
echo === Failed Runs (Last 5) ===
gh run list --repo %REPO% --status failure --limit 5

echo.
echo === To view details of a specific run: ===
echo gh run view [RUN_ID] --repo %REPO%
echo.
echo === To view logs of a specific run: ===
echo gh run view [RUN_ID] --repo %REPO% --log
echo.
echo === To download logs of a failed run: ===
echo gh run download [RUN_ID] --repo %REPO%
echo.
echo === To rerun a failed workflow: ===
echo gh run rerun [RUN_ID] --repo %REPO%