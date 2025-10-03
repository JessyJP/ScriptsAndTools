# Ensure submodules are present
git submodule update --init --recursive

# Sync URLs/branches from .gitmodules → .git/config
git submodule sync --recursive

# For each submodule: fetch, pick the tracked branch, hard-reset to origin, clean
git submodule foreach --recursive '
  set -e
  echo ">>> $name at $sm_path"
  git fetch --all --prune

  # Determine branch to track: .gitmodules branch, or upstream HEAD
  b=$(git config -f "$toplevel/.gitmodules" submodule.$name.branch || true)
  if [ -z "$b" ] || [ "$b" = "HEAD" ]; then
    b=$(git remote show origin | sed -n "/HEAD branch/s/.*: //p")
  fi
  if [ -z "$b" ]; then b=main; fi  # fallback

  # Move to that branch and hard sync to remote (handles force-push)
  git checkout -B "$b" "origin/$b" || git checkout -B "$b"
  git reset --hard "origin/$b"
  git clean -fdx
'

# Stage the updated submodule pointers in the superproject
git add .
# NOTE: automatically making the commit is optional!
git commit -m "Sync submodules to latest remote state after upstream force-push"
