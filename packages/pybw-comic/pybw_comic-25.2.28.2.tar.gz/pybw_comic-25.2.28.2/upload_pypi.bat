@echo off

echo.
echo ***********************
echo * Confirm to continue *
echo ***********************
echo.
pause
echo.

echo [1] rm old files; copy new pybw_comic dir
rmdir /s /q build dist pybw_comic.egg-info > nul
rmdir /s /q pybw_comic > nul
xcopy /e /h /i ..\pybw_comic pybw_comic > nul
echo.

echo [2] run setup.py
python setup.py sdist bdist_wheel > nul
echo.

echo [3] upload to pypi
echo.
twine upload dist/* 
echo.

pause

