@echo off
REM Git Release Batch Wrapper for LHAtoLCSC
REM This provides easy access to the PowerShell release script

setlocal EnableDelayedExpansion

REM Check if PowerShell is available
powershell -Command "Get-Host" >nul 2>&1
if errorlevel 1 (
    echo Error: PowerShell is not available
    exit /b 1
)

REM Check for help request
if "%1"=="--help" (
    echo.
    echo Git Release Script for LHAtoLCSC
    echo.
    echo Usage:
    echo   git_release.bat patch "Bug fixes" [options]
    echo   git_release.bat minor "New features" [options]
    echo   git_release.bat major "Breaking changes" [options]
    echo   git_release.bat version 0.2.4 "Specific version" [options]
    echo.
    echo Options:
    echo   --commit-all    Commit all changed files
    echo   --push         Push to remote after tagging
    echo   --create-release Create GitHub release
    echo   --dry-run      Show what would be done
    echo   --force        Force operations
    echo.
    echo Examples:
    echo   git_release.bat patch "Fixed pagination bugs" --commit-all --push
    echo   git_release.bat minor "Added currency persistence" --create-release
    echo   git_release.bat version 0.3.0 "Major UI improvements" --dry-run
    echo.
    exit /b 0
)

REM Check minimum arguments
if "%2"=="" (
    echo Error: Missing required arguments
    echo Usage: git_release.bat ^<bump_type^|version^> ^<version_or_message^> [message] [options]
    echo Run "git_release.bat --help" for more information
    exit /b 1
)

REM Parse arguments
set "bump_type=%1"
set "version_or_message=%2"
set "message=%3"
set "options="

REM Collect additional options
:parse_options
shift
shift
shift
if "%1"=="" goto :execute_release

set "options=%options% %1"
goto :parse_options

:execute_release

REM Determine if first argument is a version number or bump type
echo %version_or_message% | findstr /R /C:"^[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*$" >nul
if errorlevel 1 (
    REM Not a version number, treat as bump type
    if "%bump_type%"=="patch" (
        set "ps_cmd=powershell -ExecutionPolicy Bypass -File "%~dp0git_release.ps1" -Bump patch -Message "%version_or_message%" %options%"
    ) else if "%bump_type%"=="minor" (
        set "ps_cmd=powershell -ExecutionPolicy Bypass -File "%~dp0git_release.ps1" -Bump minor -Message "%version_or_message%" %options%"
    ) else if "%bump_type%"=="major" (
        set "ps_cmd=powershell -ExecutionPolicy Bypass -File "%~dp0git_release.ps1" -Bump major -Message "%version_or_message%" %options%"
    ) else if "%bump_type%"=="version" (
        if "%message%"=="" (
            echo Error: Version releases require a message
            echo Usage: git_release.bat version ^<version^> ^<message^> [options]
            exit /b 1
        )
        set "ps_cmd=powershell -ExecutionPolicy Bypass -File "%~dp0git_release.ps1" -Version "%version_or_message%" -Message "%message%" %options%"
    ) else (
        echo Error: Invalid bump type. Use 'patch', 'minor', 'major', or 'version'
        exit /b 1
    )
) else (
    REM It's a version number
    set "ps_cmd=powershell -ExecutionPolicy Bypass -File "%~dp0git_release.ps1" -Version "%version_or_message%" -Message "%message%" %options%"
)

REM Execute PowerShell command
echo Executing: %ps_cmd%
echo.
%ps_cmd%

if errorlevel 1 (
    echo.
    echo Release process failed!
    exit /b 1
) else (
    echo.
    echo Release process completed successfully!
)

endlocal