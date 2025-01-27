#!/bin/bash

# Check if a file name is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <html_file>"
  exit 1
fi

# Input HTML file
input_file="$1"

# Output file
output_file="episodes.txt"

# Extract lines containing 'heinetwork.tv/episode/' and save to output file
grep -o 'heinetwork\.tv/episode/[^"]*' "$input_file" > "$output_file"

# Inform the user
echo "Episodes extracted to $output_file"
