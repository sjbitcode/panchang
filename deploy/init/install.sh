# Install Docker.
echo -e "\n-- Installing docker remote server --"
wget -qO- https://get.docker.com/ | sh

# Add User to the 'docker' group.
echo -e "\n-- Adding current user to docker group --"
sudo usermod -aG docker $(whoami)

# Install pip.
echo -e "\n-- Installing Python-pip --"
apt-get -y install python3-pip

# Install Docker Compose.
echo -e "\n-- Installing docker compose --"
pip3 install docker-compose
