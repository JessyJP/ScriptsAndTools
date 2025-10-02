"""
Author: JessyJP
File: find_and_replace.py
Description: Bulk find-and-replace utility for source files. 
             Recursively processes files in a given directory and 
             replaces all occurrences of a target string with a new string.
             Supports file filtering using optional flags:
               -b, --begins   : Only process files whose names begin with a given string
               -e, --ends     : Only process files whose names end with a given string
               -c, --contains : Only process files whose names contain a given string

Recommendations for a more comprehensive app can be found here: https://github.com/JessyJP/Replace-Text-In-Files 

Also, please have a look at the standard Linux file & Text Processing Tools:
- grep       → Search text in files.
- sed        → Stream editor for inline text replacement.
- awk        → Powerful text processing & reporting.
- cut, sort, uniq → Common text manipulation.
- less / more → File viewing.
- find       → Locate files with conditions.
- fd         → Modern replacement for find.
- ripgrep (rg) → Modern, faster alternative to grep.

"""

import os
import sys
import argparse


def find_and_replace_in_file(filepath, old_string, new_string):
    """
    Process a single file, replacing old_string with new_string in each line.
    """
    with open(filepath, 'r', encoding="utf-8") as file:
        lines = file.readlines()

    with open(filepath, 'w', encoding="utf-8") as file:
        for line in lines:
            new_line = line.replace(old_string, new_string)
            file.write(new_line)


def file_matches(filename, filter_type, filter_value):
    """
    Check if the filename matches the filter condition.
    """
    if not filter_type or not filter_value:
        return True  # no filter -> always match

    if filter_type == "begins":
        return filename.startswith(filter_value)
    elif filter_type == "ends":
        return filename.endswith(filter_value)
    elif filter_type == "contains":
        return filter_value in filename

    return True


def process_files(directory, old_string, new_string, filter_type=None, filter_value=None):
    """
    Loop over files in the directory and process them if they match filter.
    """
    for subdir, _, files in os.walk(directory):
        for file in files:
            if file_matches(file, filter_type, filter_value):
                filepath = os.path.join(subdir, file)
                find_and_replace_in_file(filepath, old_string, new_string)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bulk find-and-replace utility with file filtering.")
    parser.add_argument("directory", help="Target directory to process")
    parser.add_argument("old_string", help="String to be replaced")
    parser.add_argument("new_string", help="String to replace with")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-b", "--begins", help="Only process files whose names begin with this string")
    group.add_argument("-e", "--ends", help="Only process files whose names end with this string")
    group.add_argument("-c", "--contains", help="Only process files whose names contain this string")

    args = parser.parse_args()

    # Determine filter type and value
    filter_type, filter_value = None, None
    if args.begins:
        filter_type, filter_value = "begins", args.begins
    elif args.ends:
        filter_type, filter_value = "ends", args.ends
    elif args.contains:
        filter_type, filter_value = "contains", args.contains

    process_files(args.directory, args.old_string, args.new_string, filter_type, filter_value)
