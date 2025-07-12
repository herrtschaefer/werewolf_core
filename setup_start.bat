@echo off
setlocal
:: 1. Prüfen ob venv existiert
if not exist venv (
    echo [*] Erstelle virtuelles Environment ...
    python -m venv venv
)

:: 2. Aktivieren
call venv\Scripts\activate

:: 3. Prüfen ob Pakete installiert sind
for /f %%i in ('pip list ^| findstr /c:"Package" /v ^| find /c /v ""') do set COUNT=%%i

if %COUNT%==0 (
    echo.
    echo [*] Welches Requirements-File soll installiert werden?
    echo [1] Normale requirements.txt
    echo [2] Entwickler requirements-dev.txt
    set /p REQTYPE=Bitte wählen [1/2]:

    if "%REQTYPE%"=="1" (
        if exist requirements.txt (
            echo [*] Installiere requirements.txt ...
            pip install -r requirements.txt
        ) else (
            echo [!] requirements.txt nicht gefunden!
        )
    ) else if "%REQTYPE%"=="2" (
        if exist requirements-dev.txt (
            echo [*] Installiere requirements-dev.txt ...
            pip install -r requirements-dev.txt
        ) else (
            echo [!] requirements-dev.txt nicht gefunden!
        )
    ) else (
        echo [!] Ungültige Eingabe. Überspringe Installation.
    )
) else (
    echo [*] Pakete bereits installiert – überspringe Installation.
)
echo.

if exist main.py (
    set /p RUNMAIN=Möchtest du main.py ausführen? [J/N]:

    if /i "%RUNMAIN%"=="J" (
        echo [*] Starte main.py ...
        python main.py
    )
) else (
    echo [!] main.py wurde nicht gefunden. Überspringe Ausführung.
)

echo.
echo [*] Virtuelle Umgebung aktiviert. Du kannst nun loslegen.
cmd /k