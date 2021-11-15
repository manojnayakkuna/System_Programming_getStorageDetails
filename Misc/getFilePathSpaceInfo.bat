@echo off
setlocal disabledelayedexpansion

set "folder=%~1"
if not defined folder set "folder=%cd%"

for /d %%a in ("%folder%\*") do (
	set "size=0"
	for /f "tokens=3,5" %%b in ('dir /-c /a /w /s "%%~fa\*" 2^>nul ^| findstr /b /c:"  "') do if "%%~c"=="" set "size=%%~b"
	setlocal enabledelayedexpansion
	echo(%%~nxa # !size!
	endlocal
)

endlocal