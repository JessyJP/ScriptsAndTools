#!/usr/bin/env python3

import sys
import os
import argparse
import curses
from curses import wrapper
import logging
from tqdm import tqdm

# Add the current script directory to sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from git_operations import get_git_repo, search_branches, file_commits, substring_commits, fetch_all_commits, filter_commits, get_commit_info, GITPYTHON_AVAILABLE
from visualization import interactive_mode

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main():
    logger.debug("Starting main function.")
    parser = argparse.ArgumentParser(description="GitFind - A tool for searching Git commits.")
    parser.add_argument("command", choices=["branch-search", "search-commits", "file-commits", "substring-commits"], nargs="?", help="Command to run")
    parser.add_argument("argument", nargs="?", help="Argument for the command")
    parser.add_argument("-m", "--min-char-length", type=int, default=0, help="Minimum character length to start searching (default: 0)")
    parser.add_argument("-n", "--num-commits", type=int, default=10, help="Number of commits to display (default: 10)")
    parser.add_argument("-o", "--sort-order", choices=["chronological", "reverse-chronological"], default="chronological", help="Sort order for commits (default: chronological)")
    parser.add_argument("-d", "--sort-direction", choices=["asc", "desc"], default="desc", help="Sort direction for commits (default: desc)")
    parser.add_argument("-r", "--regex", action="store_true", help="Enable regular expression search")

    args = parser.parse_args()

    if args.command:
        repo = get_git_repo() if GITPYTHON_AVAILABLE else None
        if args.command == "branch-search":
            if args.argument:
                search_branches(args.argument)
            else:
                print("Error: branch-search requires a branch name argument.")
                sys.exit(1)
        elif args.command == "search-commits":
            if args.argument:
                all_commits = fetch_all_commits(repo)
                with tqdm(total=args.num_commits, desc="Filtering commits") as progress_bar:
                    filtered_commits = filter_commits(all_commits, args.argument, args.num_commits, args.regex, repo)
                for commit in filtered_commits:
                    print(get_commit_info(commit, repo))
            else:
                print("Error: search-commits requires a search keyword argument.")
                sys.exit(1)
        elif args.command == "file-commits":
            if args.argument:
                commits = file_commits(repo, args.argument, args.num_commits, args.sort_order, args.sort_direction)
                for commit in commits:
                    print(get_commit_info(commit, repo))
            else:
                print("Error: file-commits requires a file path argument.")
                sys.exit(1)
        elif args.command == "substring-commits":
            if args.argument:
                commits = substring_commits(repo, args.argument, args.num_commits, args.sort_order, args.sort_direction)
                for commit in commits:
                    print(get_commit_info(commit, repo))
            else:
                print("Error: substring-commits requires a substring argument.")
                sys.exit(1)
    else:
        print("Entering interactive mode. Press Ctrl+C to exit.")
        wrapper(interactive_mode, args.min_char_length, args.num_commits, args.sort_order, args.sort_direction, args.regex)

if __name__ == "__main__":
    main()
