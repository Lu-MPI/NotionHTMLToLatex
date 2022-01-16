@ECHO OFF

pushd %~dp0

REM Command file for Build pip

if "%1" == "" goto fast

if "%1" == "help" goto help

if "%1" == "fast" goto fast

if "%1" == "build" goto build

if "%1" == "clear" goto clear

if "%1" == "testupload" goto testupload

if "%1" == "upload" goto upload

if "%1" == "testinstall" goto testinstall

if "%1" == "install" goto install

:help
echo " make help"
echo " make fast | build | clear                                            "
echo "      fast: build and install (use older way but fast)                "
echo "      build: build and install (use new way but slow, use for upload) "
echo "      clear: uninstall                                                "
echo " make upload | testupload                                             "
echo "      upload: upload to pypi                                          "
echo "      testupload: upload to testpypi                                  "
echo " make install | testinstall                                           "
echo "      install: install from pypi                                      "
echo "      testinstall: install from testpypi                              "
goto end

:fast
pip uninstall no2ml -y
@REM old way but fast
python setup.py sdist bdist_wheel
FOR %%i in (dist\*.whl) DO pip install %%i
goto end

:build
pip uninstall no2ml -y
@REM new way but slow
python -m build
FOR %%i in (dist\*.whl) DO pip install %%i
goto end

:clear
pip uninstall no2ml -y
goto end

:testupload
twine upload --repository testpypi dist/*
goto end

:upload
twine upload --repository pypi dist/*
goto end

:testinstall
pip uninstall no2ml -y
pip install --index-url https://test.pypi.org/simple/ --no-deps no2ml
goto end

:install
pip uninstall no2ml -y
pip install --no-deps no2ml
goto end


:end
popd