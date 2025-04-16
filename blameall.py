#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys
import shlex
from collections import Counter

# ----------------------------------
# PARAMETERS
# ----------------------------------
# Define configuration parameters for Git Blame Statistics Application.
# UPDATE_INTERVAL: display progress after processing every UPDATE_INTERVAL files.
UPDATE_INTERVAL = 1


# ----------------------------------
# CORE
# ----------------------------------
# This section contains core functions for file operations and blame statistics computation.

def get_repo_root():
    """Determine the root directory of the Git repository."""
    try:
        root = subprocess.check_output("git rev-parse --show-toplevel", shell=True, text=True).strip()
        return os.path.abspath(root)
    except subprocess.CalledProcessError:
        print("Error: Not a Git repository or Git is not installed.")
        sys.exit(1)


def get_git_tracked_files(ignore_exts):
    """Get a set of all tracked files using 'git ls-files', filtering by ignore_exts."""
    try:
        files = subprocess.check_output("git ls-files", shell=True, text=True).splitlines()
        # Convert files to absolute paths using the repository root.
        repo_root = os.getcwd()  # Already in repo root because of main()
        tracked = {os.path.abspath(os.path.join(repo_root, f)) for f in files if not any(f.endswith(ext) for ext in ignore_exts)}
        return tracked
    except subprocess.CalledProcessError:
        print("Error: Not a Git repository or Git is not installed.")
        sys.exit(1)


def filter_tracked_files(tracked_files, filter_paths):
    """
    Filter the set of tracked files using the user-supplied file or directory paths.
    Each filter is normalized to an absolute path and used to retain only those tracked files
    that match. If a filter is a directory, all files within that directory are kept.
    """
    filtered = set()
    normalized_filters = [os.path.abspath(path) for path in filter_paths]

    for file in tracked_files:
        for filt in normalized_filters:
            # Include file if the filter is a directory and file is inside it.
            if os.path.isdir(filt) and file.startswith(filt + os.sep):
                filtered.add(file)
                break
            # Include file if the filter is a file and there's an exact match.
            elif os.path.isfile(filt) and file == filt:
                filtered.add(file)
                break
    return filtered


def get_blame_for_file(file):
    """
    Runs 'git blame --line-porcelain' for a given file and returns its output.
    Converts the absolute file path to a relative path (from the repository root)
    and forces blaming HEAD while ignoring whitespace-only changes.
    Uses errors='replace' to avoid UnicodeDecodeErrors.
    """
    # Convert the absolute file path to a relative one (assuming current working directory is repo root)
    rel_file = os.path.relpath(file, os.getcwd())
    # Always blame against HEAD and ignore whitespace differences (e.g. CRLF vs LF)
    if os.name == 'nt':
        # On Windows, use double quotes for the relative path.
        blame_cmd = f'git blame -w HEAD --line-porcelain "{rel_file}"'
    else:
        blame_cmd = f"git blame -w HEAD --line-porcelain {shlex.quote(rel_file)}"

    try:
        output = subprocess.check_output(
            blame_cmd, shell=True, encoding="utf-8", errors="replace"
        )
        return output
    except subprocess.CalledProcessError:
        print(f"Warning: Could not process file {file}. Skipping.")
        return ""


def process_single_file(file):
    """
    Process a single file by running git blame and extracting blame information.
    Returns a tuple of:
      - A Counter mapping each committed author to the number of lines.
      - A set of committed authors (for participation/touched count).
      - The number of lines marked as 'Not Committed Yet'.
    """
    blame_output = get_blame_for_file(file)
    file_counter = Counter()
    touched_authors = set()
    not_committed_count = 0

    for line in blame_output.splitlines():
        if line.startswith("author "):
            author = line[len("author "):].strip()
            if author == "Not Committed Yet":
                not_committed_count += 1
            else:
                file_counter[author] += 1
                touched_authors.add(author)

    return file_counter, touched_authors, not_committed_count


def compute_blame_stats(files):
    """Compute blame statistics on the list of files and update progress periodically."""
    total_files = len(files)
    if total_files == 0:
        print("No files to process.")
        return

    overall_lines = Counter()      # Total committed lines per author.
    overall_touched = Counter()    # Number of files each author participated in.
    overall_not_committed = 0      # Total 'Not Committed Yet' lines.
    files_scanned = 0

    for file in files:
        files_scanned += 1
        file_counter, touched, not_committed = process_single_file(file)
        overall_lines.update(file_counter)
        for author in touched:
            overall_touched[author] += 1
        overall_not_committed += not_committed

        if files_scanned % UPDATE_INTERVAL == 0 or files_scanned == total_files:
            print_progress(file, files_scanned, total_files, overall_lines, overall_touched, overall_not_committed)

    if files_scanned % UPDATE_INTERVAL != 0:
        print_progress(file, files_scanned, total_files, overall_lines, overall_touched, overall_not_committed)


# ----------------------------------
# UI / DISPLAY
# ----------------------------------
# This section is responsible for updating the terminal display with progress information.

def print_progress(current_file, files_scanned, total_files, overall_lines, overall_touched, overall_not_committed):
    """
    Clears the terminal screen and prints a progress update:
      - A header comment about the application.
      - The current file being processed.
      - The number and percentage of files scanned.
      - The cumulative 'Not Committed Yet' lines.
      - A table with authors, their committed line counts, files touched, and the percentage of committed lines.
    """
    # Cross-platform clear screen command.
    os.system('cls' if os.name == 'nt' else 'clear')

    print("# Git Blame Statistics Application v3.0")
    print("# Temporary progress update (replaceable output):\n")

    pct = (files_scanned / total_files) * 100 if total_files > 0 else 0
    print(f"Scanned {files_scanned} of {total_files} files ({pct:>6.2f}% completed).")
    print(f"Currently processing file: {current_file}\n")

    print(f"Not Committed Yet lines: {overall_not_committed}\n")

    total_committed = sum(overall_lines.values())
    if total_committed > 0:
        print(f"{'Author':<30} {'Lines':>8} {'Touched':>8} {'Percentage':>12}")
        print("-" * 60)
        # Display each author (sorted by line count in descending order)
        for author, lines in overall_lines.most_common():
            touched = overall_touched.get(author, 0)
            percentage = (lines / total_committed) * 100
            print(f"{author:<30} {lines:>8} {touched:>8} {percentage:>11.2f}%")
    else:
        print("No committed lines processed yet.")

    sys.stdout.flush()


# ----------------------------------
# MAIN
# ----------------------------------
# This section handles command-line argument parsing and the main execution flow.

def parse_args():
    """
    Parse command-line arguments.
    - paths: Optional list of files and/or directories to use as filters (positional).
    - --filter (-f): Alternate option to supply a list of files and/or directories for filtering.
    - --ignore (-i): Optional list of file extension patterns to ignore.
    - --root (-r): Optionally override the repository root.
    - --list (-l): List all files that would be processed and exit.
    """
    parser = argparse.ArgumentParser(
        description="Compute Git blame statistics for a Git repository."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Optional list of files and/or directories to filter the tracked files. If not provided, the whole repository is processed."
    )
    parser.add_argument(
        "-f", "--filter",
        nargs="*",
        default=[],
        help="Alternate option to supply filtering paths (files and/or directories)."
    )
    parser.add_argument(
        "-i", "--ignore",
        nargs="*",
        default=[],
        help="List of file extensions to ignore (e.g., .md .txt)."
    )
    parser.add_argument(
        "-r", "--root",
        metavar="PATH",
        default=None,
        help="Optional: specify the repository root. If not provided, the repository root is determined automatically."
    )
    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="List all files that would be processed and exit."
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Determine and switch to repository root.
    repo_root = os.path.abspath(args.root) if args.root else get_repo_root()
    os.chdir(repo_root)

    ignore_exts = args.ignore

    # Always start with all Git tracked files.
    tracked_files = get_git_tracked_files(ignore_exts)

    # Merge positional filter paths and filter paths provided by the -f/--filter option.
    filter_paths = args.paths + args.filter
    files_to_process = (
        filter_tracked_files(tracked_files, filter_paths)
        if filter_paths else tracked_files
    )

    if not files_to_process:
        print("No files found to process.")
        sys.exit(0)

    # If the -l/--list flag is provided, list files and exit.
    if args.list:
        for f in sorted(files_to_process):
            print(f)
        sys.exit(0)

    compute_blame_stats(list(files_to_process))


if __name__ == "__main__":
    main()
