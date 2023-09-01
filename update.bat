@echo off
rmdir /s projects\
copy D:\projects\Public\ projects
git add .
git commit -m "%*"
git push -u

