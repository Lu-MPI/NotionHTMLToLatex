@ECHO OFF

pushd %~dp0

REM Command file for Build pip

if "%1" == "" goto help

if "%1" == "help" goto help

if "%1" == "build" goto build

if "%1" == "clear" goto clear

:build
pip uninstall noml -y
@REM python setup.py sdist bdist_wheel
python -m pip install --find-links=dist\*.whl noml
goto end

:clear
pip uninstall noml -y
goto end

:help
echo "make build|clear|help"
goto end

:end
popd