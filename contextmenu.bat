@echo off
color 02
for /f "tokens=3" %%a in ('reg query HKEY_CLASSES_ROOT\.iso /ve') do set ProgID=%%a
echo BBBBB   DDDD    N   N   FFFFF  OOO
echo B    B  D   D   NN  N   F      O   O
echo BBBBB   D   D   N N N   FFFF   O   O
echo B    B  D   D   N  NN   F      O   O
echo BBBBB   DDDD    N   N   F      OOO
echo.
echo [1] Installer le menu contextuel
echo [2] Supprimer le menu contextuel
choice /C 12 /N /M "" > nul
echo.
if errorlevel 2 goto remove
if errorlevel 1 goto install

:install
echo Installation du menu contextuel...
REG ADD HKEY_CURRENT_USER\Software\Classes\%ProgID%\shell\BDNFO /f
REG ADD HKEY_CURRENT_USER\Software\Classes\%ProgID%\shell\BDNFO /v icon /d "%cd%\BDNFO.exe,0" /f
REG ADD HKEY_CURRENT_USER\Software\Classes\%ProgID%\shell\BDNFO\command /f
REG ADD HKEY_CURRENT_USER\Software\Classes\%ProgID%\shell\BDNFO\command /ve /d "%cd%\BDNFO.exe """%%1"""" /f
goto end

:remove
echo Suppression du menu contextuel...
REG DELETE HKEY_CURRENT_USER\Software\Classes\%ProgID%\shell\BDNFO /f
goto end

:end
echo Termine
pause