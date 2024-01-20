@echo off
for /f %%a in ('git branch --show-current') do (
    set "branch=%%a"
)
git add .
git commit -m %1
git push https://github.com/Felifelps/Biblioteca %branch%
