#!/bin/bash

if command -v fastfetch &>/dev/null; then
    fastfetch  # Run fastfetch if it is installed
elif command -v neofetch &>/dev/null; then
    neofetch   # Fall back to neofetch if fastfetch is not available
fi