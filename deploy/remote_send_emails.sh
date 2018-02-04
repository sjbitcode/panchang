#!/usr/bin/env bash

USER=deploy

# Get absolute path of the script.
PARENT_PATH=$( cd "$(dirname "${BASH_SOURCE}")" ; pwd -P )
ROOT_PATH=$( cd "$(dirname "${PARENT_PATH}")" ; pwd -P )

# Load HOST config.
source "$PARENT_PATH/_host.sh"
echo -e "-- Deploying application on $HOST --\n"

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

# dc run --rm worker python -m panchang.send_emails

# Docker compose file location.
COMPOSE_PROD="/home/$USER/docker-compose-prod.yml"

# Run send_emails one time.
SEND_EMAILS="docker-compose -f $COMPOSE_PROD run --rm worker python -m panchang.send_emails"

# Execute deploy command.
ssh -i $KEY $USER@$HOST $SEND_EMAILS

echo -e "\n-- Emails sent on $HOST --"
