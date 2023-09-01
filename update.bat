@echo off
rmdir /S /Q projects\
mkdir projects
xcopy D:\projects\Public\ projects /E
git add .
git commit -m "%*"
git push -u

