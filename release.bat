@echo off
REM Quick Release Script for LHAtoLCSC
REM Usage: release.bat [patch|minor|major]

setlocal

REM Check if argument provided
if "%1"=="" (
    echo Usage: release.bat [patch^|minor^|major]
    echo.
    echo Examples:
    echo   release.bat patch    ^(0.2.0 -^> 0.2.1^)
    echo   release.bat minor    ^(0.2.0 -^> 0.3.0^)
    echo   release.bat major    ^(0.2.0 -^> 1.0.0^)
    exit /b 1
)

REM Validate bump type
if not "%1"=="patch" if not "%1"=="minor" if not "%1"=="major" (
    echo Error: Invalid bump type "%1"
    echo Must be one of: patch, minor, major
    exit /b 1
)

echo.
echo ========================================
echo LHAtoLCSC Release Workflow
echo ========================================
echo.
echo Bump type: %1
echo.

REM Run release workflow
python release_workflow.py %1

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================
    echo Release FAILED!
    echo ========================================
    exit /b 1
)

echo.
echo ========================================
echo Release COMPLETED Successfully!
echo ========================================
echo.

endlocal
