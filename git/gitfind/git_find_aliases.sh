# Search and show branches by name
alias git-branch-search='git branch -a | grep'

# Show all commits that match summary, description, or commit ID
alias git-search-commits='git log --all --grep'

# Show all commits that pertain to a file
alias git-file-commits='git log --follow --pretty=format:"%h %ad | %s%d [%an]" --date=short --'

# Show all commits that contain a substring
alias git-substring-commits='git log --all --pretty=format:"%h %ad | %s%d [%an]" --date=short | grep'
