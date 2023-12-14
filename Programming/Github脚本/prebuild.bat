set dep_base=..\..\deps\
set bin_base=..\..\bin\

rmdir /Q /S %bin_base%
rmdir /Q /S %dep_base%

mkdir %dep_base%include
mkdir %dep_base%lib

set src_base=..\..\..\

set lib_name=libflow
mkdir %dep_base%include\%lib_name%
xcopy %src_base%%lib_name%\include %dep_base%include\%lib_name% /S /Y /C
xcopy %src_base%%lib_name%\bin %dep_base%lib /S /Y /C
