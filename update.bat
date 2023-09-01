@echo off
rm -r projects/
cp -r D:\projects\Public\ projects
git add .
git commit -m "%*"
git push -u

