#!/usr/bin/env bash

USER=deploy

# Get absolute path of the script.
PARENT_PATH=$( cd "$(dirname "${BASH_SOURCE}")" ; pwd -P )
ROOT_PATH=$( cd "$(dirname "${PARENT_PATH}")" ; pwd -P )

# Load HOST config.
source "$ROOT_PATH/_host.sh"
echo -e "-- Provisioning server @ $HOST --\n"


# Check the existence of the env argument.
if [[ $# -eq 0 ]] ; then
    KEY="$HOME/.ssh/id_rsa"
    echo "   Using default private key: $KEY"
else
    # Build private key location.
    KEY="$ROOT_PATH/keys/$1/$1"
    echo "  Using private key: $KEY"
fi

# If specified env directory exists, then make
# the same directories on the remote server.
if [ ! -f "$KEY" ]; then
    echo -e "\n\n! Private key: $KEY does not exist !"
    exit 1
fi


# LOCKDOWN
# Copy 'lockdown.sh' script to the remote server.
echo -e "\n-- Copying lockdown script to remote server --"
LOCAL_LOCKDOWN_SCRIPT="$PARENT_PATH/lockdown.sh"
REMOTE_LOCKDOWN_SCRIPT="/root/lockdown.sh"
scp -i $KEY $LOCAL_LOCKDOWN_SCRIPT root@$HOST:$REMOTE_LOCKDOWN_SCRIPT

# Execute the 'lockdown.sh' script.
echo -e "\n-- Running lockdown script on remote server --"
ssh -i $KEY root@$HOST bash $REMOTE_LOCKDOWN_SCRIPT
sleep 2


# INSTALL
# Copy 'install.sh' script to remote server.
echo -e "\n-- Copying install script to remote server --"
LOCAL_INSTALL_SCRIPT="$PARENT_PATH/install.sh"
REMOTE_INSTALL_SCRIPT="/home/$USER/install.sh"
scp -i $KEY $LOCAL_INSTALL_SCRIPT $USER@$HOST:$REMOTE_INSTALL_SCRIPT

# After the 'lockdown.sh' script runs, the user 'deploy'
# should be created with root privilages. We continue the
# server provision with the newly created user 'deploy.'
echo -e "\n-- Running install script on remote server --"
ssh -i $KEY $USER@$HOST sudo bash $REMOTE_INSTALL_SCRIPT
ssh -i $KEY $USER@$HOST rm $REMOTE_INSTALL_SCRIPT


echo -e "\n-- Server @ $HOST has been provisioned --"
