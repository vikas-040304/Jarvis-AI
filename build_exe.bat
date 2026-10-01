@echo off
REM build_exe.bat
REM Builds jarvis_background.py into a single standalone .exe with NO console
REM window - double-click it to run Jarvis in the background, just like a
REM normal Windows app.

echo Building Jarvis.exe ...
py -3.13 -m PyInstaller --onefile --noconsole --name Jarvis jarvis_background.py

echo.
echo Done. Find Jarvis.exe inside the "dist" folder.
echo You can copy Jarvis.exe anywhere and double-click it to run - no terminal needed.
pause
