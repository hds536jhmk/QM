@echo off
pyinstaller main.pyw ^
	--clean ^
	--noconfirm ^
	--noconsole ^
	--nowindow ^
	--name "QM" ^
	--distpath ./build/dist ^
	--workpath ./build/tmp ^
	--specpath ./build ^
	--add-data ../questions;./questions ^
	--add-data ../settings.json;./ ^
	--add-data ../logo.ico;./ ^
	--icon ../logo.ico
pause