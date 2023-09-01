@echo off
git add .
git add --rename D:\projects\Public projects
git commit -m "%*"
git push -u
