import subprocess
import os
import re
import sys
import logging
from tqdm import tqdm

try:
    import git
    GITPYTHON_AVAILABLE = True
except ImportError:
    GITPYTHON_AVAILABLE = False

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def run_command(command):
    logger.debug(f"Running command: {command}")
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout.strip(), result.stderr.strip()

def get_git_repo():
    logger.debug("Getting Git repository.")
    try:
        repo = git.Repo(search_parent_directories=True)
        return repo
    except git.exc.InvalidGitRepositoryError:
        logger.error("Error: Not a valid Git repository.")
        sys.exit(1)

def get_git_stats():
    logger.debug("Getting Git stats.")
    if GITPYTHON_AVAILABLE:
        repo = get_git_repo()
        repo_name = os.path.basename(repo.working_tree_dir)
        current_branch = repo.active_branch.name
        remote_urls = "\n".join([str(remote) for remote in repo.remotes])
    else:
        repo_name, _ = run_command("basename `git rev-parse --show-toplevel`")
        current_branch, _ = run_command("git rev-parse --abbrev-ref HEAD")
        remote_urls, _ = run_command("git remote -v")
    return repo_name, current_branch, remote_urls

def fetch_all_commits(repo=None):
    logger.debug("Fetching all commits.")
    if GITPYTHON_AVAILABLE and repo:
        commits = list(repo.iter_commits('--all'))
    else:
        commits_output, _ = run_command("git log --all --pretty=format:'%H'")
        commit_hashes = commits_output.split()
        commits = [commit_hash.strip() for commit_hash in commit_hashes]
    return commits

def filter_commits(commits, search_keyword, num_commits, regex, repo=None):
    logger.debug("Filtering commits.")
    filtered_commits = []
    progress_bar = tqdm(total=num_commits, desc="Filtering commits")
    try:
        if GITPYTHON_AVAILABLE and repo:
            for commit in commits:
                message = commit.message
                if regex:
                    if re.search(search_keyword, message):
                        filtered_commits.append(commit)
                else:
                    if search_keyword.lower() in message.lower():
                        filtered_commits.append(commit)
                if len(filtered_commits) >= num_commits:
                    break
                progress_bar.update(1)
        else:
            for commit_hash in commits:
                commit_message, _ = run_command(f"git log -1 --pretty=%B {commit_hash}")
                if regex:
                    if re.search(search_keyword, commit_message):
                        filtered_commits.append(commit_hash)
                else:
                    if search_keyword.lower() in commit_message.lower():
                        filtered_commits.append(commit_hash)
                if len(filtered_commits) >= num_commits:
                    break
                progress_bar.update(1)
    finally:
        progress_bar.close()
    return filtered_commits

def get_commit_info(commit, repo=None):
    if GITPYTHON_AVAILABLE and repo:
        return f"{commit.hexsha[:7]} {commit.committed_datetime.date()} | {commit.summary} [{commit.author}]"
    else:
        commit_info, _ = run_command(f"git show -s --format='%h %ad | %s [%an]' --date=short {commit}")
        return commit_info

def search_branches(branch_name):
    logger.debug(f"Searching for branch: {branch_name}")
    if GITPYTHON_AVAILABLE:
        repo = get_git_repo()
        branches = [branch.name for branch in repo.branches if branch_name in branch.name]
        if branches:
            for branch in branches:
                print(f"Found branch: {branch}")
        else:
            print(f"No branches found with the name: {branch_name}")
    else:
        output, _ = run_command(f"git branch --list *{branch_name}*")
        if output:
            print(output)
        else:
            print(f"No branches found with the name: {branch_name}")

# Add other functions that you need, e.g., file_commits, substring_commits, etc.
