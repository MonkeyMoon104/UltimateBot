@echo off
for /f "tokens=2 delims=[]" %%a in ('ver') do set VERSION=%%a
if %VERSION:~0,2% GEQ 10 (
    reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1
)

for /f %%a in ('echo prompt $E ^| cmd') do set "ESC=%%a"

set "RED=%ESC%[91m"
set "GREEN=%ESC%[92m"
set "YELLOW=%ESC%[93m"
set "BLUE=%ESC%[94m"
set "MAGENTA=%ESC%[95m"
set "CYAN=%ESC%[96m"
set "RESET=%ESC%[0m"


cls
echo %CYAN%=============================================================================%RESET%
echo %CYAN%              MonkeyMoon104%RESET%
echo %CYAN%               Obfuscating%RESET%
echo %CYAN%=============================================================================%RESET%
echo %MAGENTA%           Welcome to the Ultimate Bot Obfuscation Utility%RESET%
echo %MAGENTA%                  Powered by PyArmor 8+ and Windows Batch%RESET%
echo.

echo %BLUE%[1/8]%RESET% %YELLOW%Scanning for 'requirements.txt'...%RESET%
if exist requirements.txt (
    echo %GREEN%  -> Found 'requirements.txt'. Dependencies appear present.%RESET%
) else (
    echo %RED%  -> 'requirements.txt' NOT FOUND. Please make sure your environment is ready.%RESET%
)
timeout /t 1 >nul
echo.

echo %BLUE%[2/8]%RESET% %YELLOW%Verifying Python installation...%RESET%
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo %RED%  -> Python not found in PATH! Install it or update your PATH.%RESET%
    pause
    exit /b
) else (
    python --version
    echo %GREEN%  -> Python detected successfully.%RESET%
)
timeout /t 1 >nul
echo.

echo %BLUE%[3/8]%RESET% %YELLOW%Checking for previous obfuscation output...%RESET%
if exist obfuscated_out (
    echo %MAGENTA%  -> Removing old 'obfuscated_out' directory...%RESET%
    rmdir /s /q obfuscated_out
) else (
    echo %GREEN%  -> No existing 'obfuscated_out' found. Skipping clean step.%RESET%
)
timeout /t 1 >nul
echo.

echo %BLUE%[4/8]%RESET% %YELLOW%Creating clean output folder...%RESET%
echo %GREEN%  -> Directory 'obfuscated_out' created successfully.%RESET%
timeout /t 1 >nul
echo.

echo %BLUE%[5/8]%RESET% %YELLOW%Preparing PyArmor for obfuscation...%RESET%
where pyarmor >nul 2>&1
if %errorlevel% neq 0 (
    echo %RED%  -> PyArmor is not installed! Run 'pip install pyarmor' to fix.%RESET%
    pause
    exit /b
) else (
    pyarmor --version
    echo %GREEN%  -> PyArmor ready.%RESET%
)
timeout /t 1 >nul
echo.

echo %BLUE%[6/8]%RESET% %YELLOW%Running full obfuscation process...%RESET%
pyarmor gen -O obfuscated_out .
if %errorlevel% neq 0 (
    echo %RED%  -> Obfuscation process failed. Fix errors above and try again.%RESET%
    pause
    exit /b
)
echo %GREEN%  -> Obfuscation completed without errors.%RESET%
timeout /t 1 >nul
echo.

echo %BLUE%[7/8]%RESET% %YELLOW%Finalizing project...%RESET%
echo %MAGENTA%  -> Project 'Ultimate Bot' successfully protected and ready for deployment.%RESET%
timeout /t 1 >nul
echo.

echo %BLUE%[8/8]%RESET% %CYAN%Execution command:%RESET%
echo.
echo cd obfuscated_out && python UltimateBot.py
echo.

echo %CYAN%=============================================================================%RESET%
echo %GREEN%        The Ultimate Bot is now secured and ready to launch!%RESET%
echo %GREEN%        You can copy the obfuscated_out folder to your server.%RESET%
echo %CYAN%=============================================================================%RESET%
echo.
pause
