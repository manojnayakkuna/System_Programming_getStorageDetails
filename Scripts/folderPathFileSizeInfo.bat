@echo off
echo %1
echo %2
set argument1=%1
set argument2=%2
echo Getting folderPath file sizes for you...storing to %argument1%

setlocal disabledelayedexpansion
if EXIST %argument1% del %argument1%
echo File,Bytes Size,Short Size > %argument1%

set "folderPath=%argument2%"
  if not defined folderPath set "folderPath=%cd%"

    dir /s /A:-D > %argument1%

endlocal
exit /b