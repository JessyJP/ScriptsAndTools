#!/bin/bash

# Description: Checks if the `onefetch` tool is installed. If available, runs it
#              to display repository information about the current Git project.
#              If not installed, it provides a message with installation details.
# Author: JessyJP
# Dependencies: onefetch (https://github.com/o2sh/onefetch)

# Check if onefetch is installed
if command -v onefetch &> /dev/null
then
    # onefetch is installed, call it on the current directory
    onefetch
else
    echo "To get info about the git project please install 'onefetch' from https://github.com/o2sh/onefetch."
fi
