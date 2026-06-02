@echo off
REM Abre o Dashboard de Orcamento no navegador padrao via servidor local.
REM Usa Python (ja vem com Windows na maioria dos casos) na porta 8766.
REM Se nao tiver Python, instalar: https://www.python.org/downloads/

cd /d "%~dp0"
echo.
echo  Silva Pimenta + Magalhaes Gomes - Dashboard de Orcamento
echo  Servidor local: http://localhost:8766
echo.
echo  CTRL+C pra fechar
echo.

REM Tenta py.exe (Python Launcher) primeiro, que e mais confiavel no Windows.
REM Depois cai pro caminho explicito, e por ultimo pro python no PATH.
where py >nul 2>nul
if %ERRORLEVEL%==0 (
    start "" http://localhost:8766
    py -m http.server 8766
) else if exist "C:\Users\silva\AppData\Local\Python\pythoncore-3.14-64\python.exe" (
    start "" http://localhost:8766
    "C:\Users\silva\AppData\Local\Python\pythoncore-3.14-64\python.exe" -m http.server 8766
) else (
    where python >nul 2>nul
    if %ERRORLEVEL%==0 (
        start "" http://localhost:8766
        python -m http.server 8766
    ) else (
        echo  Python nao encontrado. Instalar: https://www.python.org/downloads/
        pause
    )
)
