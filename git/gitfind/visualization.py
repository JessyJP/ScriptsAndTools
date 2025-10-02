import curses
import logging
from tqdm import tqdm
from .git_operations import get_git_stats, fetch_all_commits, filter_commits, get_commit_info, get_git_repo, GITPYTHON_AVAILABLE

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def print_git_stats(stdscr, min_char_length, num_commits, sort_order, sort_direction, regex):
    logger.debug("Printing Git stats.")
    repo_name, current_branch, remote_urls = get_git_stats()
    stdscr.addstr(0, 0, f"Repository: {repo_name}")
    stdscr.addstr(1, 0, f"Current Branch: {current_branch}")
    stdscr.addstr(2, 0, "Remote URLs:")
    for i, line in enumerate(remote_urls.split('\n')):
        stdscr.addstr(3 + i, 0, line)
    stdscr.addstr(5 + i, 0, f"Min Char Length: {min_char_length}")
    stdscr.addstr(6 + i, 0, f"Num Commits: {num_commits}")
    stdscr.addstr(7 + i, 0, f"Sort Order: {sort_order}")
    stdscr.addstr(8 + i, 0, f"Sort Direction: {sort_direction}")
    stdscr.addstr(9 + i, 0, f"Regex Mode: {regex}")
    stdscr.addstr(11 + i, 0, "Enter search term: ")

def display_commits(stdscr, commits, repo=None):
    logger.debug("Displaying commits.")
    max_y, max_x = stdscr.getmaxyx()
    for i, commit in enumerate(commits[:max_y - 13]):  # leave space for stats and search bar
        commit_info = get_commit_info(commit, repo)
        stdscr.addstr(13 + i, 0, commit_info[:max_x - 1])  # truncate to fit screen width

def interactive_mode(stdscr, min_char_length, num_commits, sort_order, sort_direction, regex):
    logger.debug("Entering interactive mode.")
    curses.echo()
    search_term = ""
    repo = get_git_repo() if GITPYTHON_AVAILABLE else None
    all_commits = fetch_all_commits(repo)
    filtered_commits = all_commits[:num_commits]  # initially show first 'num_commits' commits

    def refresh_screen():
        stdscr.clear()
        print_git_stats(stdscr, min_char_length, num_commits, sort_order, sort_direction, regex)
        stdscr.addstr(12, 0, search_term)
        display_commits(stdscr, filtered_commits, repo)
        stdscr.refresh()

    refresh_screen()
    while True:
        char = stdscr.getch()
        if char == curses.KEY_BACKSPACE or char == 127:
            search_term = search_term[:-1]
        else:
            search_term += chr(char)

        if len(search_term) >= min_char_length:
            with tqdm(total=num_commits, desc="Filtering commits") as progress_bar:
                filtered_commits = filter_commits(all_commits, search_term, num_commits, regex, repo)
        else:
            filtered_commits = all_commits[:num_commits]

        refresh_screen()
