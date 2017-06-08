#!/usr/bin/env bash

USER=deploy

# Get absolute path of the script.
PARENT_PATH=$( cd "$(dirname "${BASH_SOURCE}")" ; pwd -P )
ROOT_PATH=$( cd "$(dirname "${PARENT_PATH}")" ; pwd -P )

# Load HOST config.
source "$PARENT_PATH/_host.sh"
echo -e "-- Updating server @ $HOST --\n"

# Check the existence of the env argument.
if [[ $# -eq 0 ]] ; then
    echo "Please specify an env (staging | prod)"
    exit
else
    # Get env argument.
    ENV=$1
    # Build private key location.
    KEY="$PARENT_PATH/keys/$ENV/$ENV"
fi

# Copy local docker-compose-prod.yml file to the remote server.
echo -e "\n-- Copying docker-compose-prod.yml to remote server --"
LOCAL_COMPOSE_PROD="$ROOT_PATH/docker-compose-prod.yml"
REMOTE_COMPOSE_PROD="/home/$USER/docker-compose-prod.yml"
scp -i $KEY $LOCAL_COMPOSE_PROD $USER@$HOST:$REMOTE_COMPOSE_PROD

# Copy env files to remote server.
echo -e "\n-- Copying $ENV env files to remote server --"
LOCAL_ENV_DIR="$PARENT_PATH/env/$ENV"
REMOTE_ENV_DIR="/home/$USER/deploy/env"

# If specified env directory exists, then make
# the same directories on the remote server.
if [ -d "$LOCAL_ENV_DIR" ]; then
    echo "-- Making remote env directories on remote server --"
    ssh -i $KEY $USER@$HOST mkdir -p $REMOTE_ENV_DIR
fi

scp -i $KEY -r $LOCAL_ENV_DIR $USER@$HOST:$REMOTE_ENV_DIR

echo -e "\n-- Server @ $HOST has been updated --"
