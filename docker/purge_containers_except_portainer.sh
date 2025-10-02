#!/bin/bash

# ======================= Stop & purge all containers =======================
echo "----------------------------------------------------------------------"
echo "Stop and remove existing containers:"
# Get list of containers to be excluded (Portainer)
container_ids=$(docker ps -aqf "name=portainer")

# List all container IDs except Portainer's
echo -e "\n""List all container IDs except Portainer's:"
echo -e "CONTAINER ID\tSTATUS\t\tNAMES" # Header for the table
docker ps --format "{{.ID}}\t{{.Status}}\t{{.Names}}" | grep -v $container_ids | \
      awk -F"\t" '{gsub(/ \(healthy\)/,"",$2); print $1"\t"$2"\t"$3}'

# Stop all containers except Portainer
echo -e "\n""Stop all containers except Portainer:"
docker stop $(docker ps -aq | grep -v $container_ids)

# Remove all stopped containers except Portainer
echo -e "\n""Remove all stopped containers except Portainer"
docker rm $(docker ps -aq | grep -v $container_ids)

# Remove all unused volumes (Note: This will not specifically target Portainer volumes unless they are unused)
#docker volume prune -f
#docker system prune -f
