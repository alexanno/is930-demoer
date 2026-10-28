@echo off
rem Starter QGIS med forenklet grensesnitt og apner Verdenskart.
rem Bruker en egen profil (skole), sa vanlig QGIS-oppsett pa maskinen rores ikke.
rem Hvis QGIS ligger et annet sted: sett QGIS_EXE for kjoring av filen.
setlocal
set "DIR=%~dp0"
if not defined QGIS_EXE (
  for /d %%D in ("C:\Program Files\QGIS*") do (
    if exist "%%D\bin\qgis-bin.exe" set "QGIS_EXE=%%D\bin\qgis-bin.exe"
    if exist "%%D\bin\qgis-ltr-bin.exe" set "QGIS_EXE=%%D\bin\qgis-ltr-bin.exe"
  )
)
if not defined QGIS_EXE (
  echo Fant ikke QGIS i C:\Program Files. Installer QGIS fra qgis.org.
  pause
  exit /b 1
)
start "" "%QGIS_EXE%" --profile skole --code "%DIR%oppsett.py" "%DIR%verdenskart-befolkning.qgz"
