#!/bin/bash

printf "%-12s     %-10s    %-15s    %s\n" "CONTAINER ID" "RAM USAGE" "IP ADDRESS" "CONTAINER NAME"
echo   "-----------------------------------------------------------------------"

docker ps --format '{{.ID}}' | while read container_id; do
    ip=$(docker inspect --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "$container_id")
    name=$(docker inspect --format '{{.Name}}' "$container_id" | sed 's/^\///')

    # Fetching memory usage using docker stats
    mem_usage=$(docker stats --no-stream --format "{{.MemUsage}}" "$container_id" | awk '{print $1}')
    # Extract the numerical part of the memory usage and format it
    mem_value=$(echo $mem_usage | grep -o -E '[0-9.]+' | head -1)
    mem_unit=$(echo $mem_usage | grep -o -E '[a-zA-Z]+' | head -1)

    # Assuming RAM usage to be formatted to 10 characters, right-aligned
    # Adjust the format if the actual length varies
    formatted_mem_usage=$(printf "%10s" "$mem_value $mem_unit")

    # Print with specified alignments and fixed-width fields
    printf "%-12s    %-10s    %-15s    %s\n" "$container_id" "$formatted_mem_usage" "$ip" "$name"
done
