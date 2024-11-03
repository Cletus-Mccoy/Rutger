@echo off
setlocal enabledelayedexpansion

REM Initial diagnostic to confirm script start
echo [DEBUG] Starting script...

REM Set the config file to .env
set "ConfigFile=.env"
echo [INFO] Config file specified: %ConfigFile%

REM Check that the specified file exists
if not exist "%ConfigFile%" (
    echo [ERROR] Specified .env file not found: %ConfigFile%
    exit /b 1
)

REM Initialize variables
set "currentTarget="
set "targets="

REM Start reading the .env file
echo [INFO] Reading .env file: %ConfigFile%
for /f "usebackq delims=" %%A in ("%ConfigFile%") do (
    set "line=%%A"
    echo [DEBUG] Processing line: !line!

    REM Ignore lines that are completely empty or only contain whitespace
    if not "!line!"=="" (
        REM Ignore lines starting with #
        if "!line:~0,1!" neq "#" (
            REM Handle key-value pairs within the current target section
            if defined currentTarget (
                echo !line!>>"!currentTarget!\.env"
                echo [DEBUG] Added key: !line! to !currentTarget!\.env
            ) else (
                echo [WARNING] Skipping key without a target: !line!
            )
        ) else (
            REM Check if the line is a section header like # [ollama]
            set "trimmedLine=!line:~2!"  REM Remove the '# ' part
            if "!trimmedLine:~0,1!"=="[" (
                set "currentTarget=!trimmedLine:~1,-1!"
                echo [INFO] Found target section: !currentTarget!

                REM Ignore target if it is [local]
                if /i "!currentTarget!"=="local" (
                    echo [INFO] Ignoring target: !currentTarget!
                    set "currentTarget="
                ) else (
                    REM Ensure folder exists, clear previous .env file
                    set "targets=!targets! !currentTarget!"
                    if not exist "!currentTarget!" (
                        mkdir "!currentTarget!"
                        echo [INFO] Created directory: !currentTarget!
                    )
                    if exist "!currentTarget!\.env" (
                        del "!currentTarget!\.env"
                        echo [INFO] Reset .env file in: !currentTarget!
                    )
                )
            )
        )
    )
)

REM Display the targets and their keys
for %%T in (%targets%) do (
    echo [INFO] Finalized .env file for target: %%T
    echo [INFO] Contents of %%T\.env:
    type %%T\.env
    echo ------------------------------
)

endlocal
