mv ../projects/Public projects
git add .
git commit -m "$*"
git push -u
rm -r projects/
ls
