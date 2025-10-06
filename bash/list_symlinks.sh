#!/usr/bin/env bash
# ==============================================================================
#  Author:        Yasen Polihronov
#  File:          list_symlinks.sh
#  Description:   Lists all symbolic links in the current repository or directory,
#                 displaying each link and its target. Highlights broken links.
# ==============================================================================

set -euo pipefail

echo "-------------------------------------------------------------------------------"
echo " Symlink overview for: $(pwd)"
echo "-------------------------------------------------------------------------------"

# Find all symlinks and print "path -> target"
find . -type l -printf '%p -> %l\n' | while read -r line; do
  link_path="${line%% -> *}"
  target_path="${line#*-> }"

  # Check if the target exists
  if [[ -e "$link_path" ]]; then
    printf "%s\n" "$line"
  else
    printf "\033[31m%s (BROKEN)\033[0m\n" "$line"
  fi
done

echo "-------------------------------------------------------------------------------"