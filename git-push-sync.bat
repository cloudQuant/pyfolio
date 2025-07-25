@echo off
REM Batch script to push to both origin and cloudquant remotes

echo Pushing to origin (Gitee)...
git push origin %*

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Syncing to cloudquant (GitHub)...
    git push cloudquant %*
    
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo Successfully pushed to both remotes!
    ) else (
        echo.
        echo Failed to push to cloudquant remote
        exit /b 1
    )
) else (
    echo.
    echo Failed to push to origin
    exit /b 1
)