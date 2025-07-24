@echo off
REM Simple test script for pyfolio across Python versions
setlocal EnableDelayedExpansion

echo ======================================== 
echo Pyfolio Python Compatibility Test
echo ======================================== 
echo.

REM Create results directory
if not exist test_results mkdir test_results

REM Create summary file
set summary=test_results\summary.txt
echo Pyfolio Test Summary > %summary%
echo Tested on: %date% %time% >> %summary%
echo. >> %summary%

REM Test each Python version
for %%v in (py38 py39 py310 py311 py312 py313) do (
    echo.
    echo Testing %%v...
    echo ----------------------------------------
    
    REM Activate environment and run tests
    call conda activate %%v 2>nul
    if errorlevel 1 (
        echo %%v: NOT FOUND - Conda environment missing >> %summary%
        echo [SKIP] %%v environment not found
    ) else (
        REM Get Python version
        for /f "tokens=*" %%p in ('python --version 2^>^&1') do set pyver=%%p
        echo Using !pyver!
        
        REM Install and test
        echo Installing dependencies...
        pip install -U -r requirements.txt >test_results\%%v_install.log 2>&1
        
        echo Installing pyfolio in development mode...
        pip install -U -e . >>test_results\%%v_install.log 2>&1
        
        echo Running tests...
        pytest tests/ -n 8 --tb=short >test_results\%%v_tests.log 2>&1
        
        if errorlevel 1 (
            echo %%v: FAILED - !pyver! >> %summary%
            echo [FAIL] Tests failed for %%v
            
            REM Extract failure summary
            findstr /C:"FAILED" /C:"ERROR" test_results\%%v_tests.log | findstr /V ".py" >> %summary%
        ) else (
            echo %%v: PASSED - !pyver! >> %summary%
            echo [PASS] All tests passed for %%v
            
            REM Extract success summary  
            findstr "passed" test_results\%%v_tests.log | findstr "==" >> %summary%
        )
        
        echo. >> %summary%
        call conda deactivate
    )
)

echo.
echo ======================================== 
echo Test Summary:
echo ======================================== 
type %summary%
echo.
echo Detailed logs: test_results\
pause