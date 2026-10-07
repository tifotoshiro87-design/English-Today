@echo off
setlocal EnableExtensions
title CAP NHAT - English Today
cd /d "%~dp0"
echo.
echo ===== CAP NHAT ENGLISH TODAY =====
echo.

where git >nul 2>nul
if errorlevel 1 goto NOGIT

for /f "usebackq delims=" %%D in (`powershell -NoProfile -Command "(New-Object -ComObject Shell.Application).NameSpace('shell:Downloads').Self.Path"`) do set "DL=%%D"
if not defined DL set "DL=%USERPROFILE%\Downloads"

set "SRC="
for /f "delims=" %%F in ('dir /b /a-d /o-d "%DL%\bai_moi*.json" 2^>nul') do if not defined SRC set "SRC=%DL%\%%F"
if not defined SRC goto NOFILE

git config user.email >nul 2>nul
if errorlevel 1 git config user.email "cap-nhat@users.noreply.github.com"
git config user.name >nul 2>nul
if errorlevel 1 git config user.name "Cap nhat"

echo [1/4] Dong bo voi GitHub...
git pull --rebase --autostash
if errorlevel 1 goto ERR

if not exist "inbox" mkdir "inbox"
for /f %%T in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd-HHmmss"') do set "TS=%%T"

echo [2/4] Lay file bai moi trong Downloads...
move /y "%SRC%" "inbox\bai_moi_%TS%.json" >nul
if errorlevel 1 goto ERR

echo [3/4] Dong goi...
git add inbox
git commit -m "bai moi %TS%"
if errorlevel 1 goto ERR

echo [4/4] Day len GitHub...
git push
if not errorlevel 1 goto OK
echo Co thay doi moi tren GitHub, dang thu lai...
git pull --rebase --autostash
if errorlevel 1 goto ERR
git push
if errorlevel 1 goto ERR

:OK
echo.
echo ===== XONG! Khoang 1-2 phut nua app co bai moi. =====
timeout /t 8 >nul
exit /b 0

:NOGIT
echo [LOI] May chua cai Git for Windows.
echo Tai ban mien phi tai: https://git-scm.com/download/win
echo Cai xong thi bam dup CAPNHAT.bat lai.
pause
exit /b 1

:NOFILE
echo [LOI] Khong thay file bai_moi.json trong thu muc Downloads.
echo Hay tai file bai_moi.json tu Claude ve truoc, roi bam lai.
pause
exit /b 1

:ERR
echo.
echo [LOI] Co su co o buoc tren. Hay chup man hinh nay gui cho Claude.
pause
exit /b 1
