#!/bin/bash

# List all Docker network IDs and store them in a variable
network_ids=$(docker network ls --quiet)

# Loop through each network ID and inspect it
for id in $network_ids; do
    echo "Inspecting network with ID: $id"
    docker network inspect $id
    echo "----------------------------------------------------"
done
