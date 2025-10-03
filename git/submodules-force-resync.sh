# Respect tracked branches and force update to remote commits
git submodule update --remote --recursive --force
git add .
git commit -m "Force-update submodules to latest remote after rewrite"
