# Note: This is for the Ubuntu 10.04 x64 image available on Digital Ocean
# and may not work for other images / OS versions.

# Warning: This script directy edits some configuration files that may
# render your OS unusable if there is an error. Use at your own risk.

AUTH_KEYS_DIR="/root"

USER="deploy"

# Create new user.
useradd $USER
mkdir /home/$USER
mkdir /home/$USER/.ssh
chmod 700 /home/$USER/.ssh
chsh -s /bin/bash $USER

# Copy Authorized keys.
cp $AUTH_KEYS_DIR/.ssh/authorized_keys /home/$USER/.ssh/authorized_keys
chmod 400 /home/$USER/.ssh/authorized_keys
chown $USER:$USER /home/$USER -R

# Add User to the 'sudo' group.
usermod -a -G sudo $USER

echo "Set password for user"
passwd $USER

apt-get update
apt-get upgrade -y
apt-get install fail2ban mosh ufw vim unattended-upgrades -y

# Add User to the sudoers file.
echo "$USER    ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Configure SSH.
cat << EOF > /etc/ssh/sshd_config
Port 22
Protocol 2
HostKey /etc/ssh/ssh_host_rsa_key
HostKey /etc/ssh/ssh_host_dsa_key
HostKey /etc/ssh/ssh_host_ecdsa_key
HostKey /etc/ssh/ssh_host_ed25519_key
UsePrivilegeSeparation yes
KeyRegenerationInterval 3600
ServerKeyBits 1024
SyslogFacility AUTH
LogLevel INFO
LoginGraceTime 120
PermitRootLogin no
StrictModes yes
RSAAuthentication yes
PubkeyAuthentication yes
IgnoreRhosts yes
RhostsRSAAuthentication no
HostbasedAuthentication no
PermitEmptyPasswords no
ChallengeResponseAuthentication no
PasswordAuthentication no
X11Forwarding yes
X11DisplayOffset 10
PrintMotd no
PrintLastLog yes
TCPKeepAlive yes
AcceptEnv LANG LC_*
Subsystem sftp /usr/lib/openssh/sftp-server
UsePAM yes
EOF

service ssh restart

# Configure Firewall.
ufw allow 22
ufw allow 80
ufw allow 443
ufw allow 60000:61000/udp
ufw --force enable

# Configure updates.
cat << EOF > /etc/apt/apt.conf.d/10periodic
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Download-Upgradeable-Packages "1";
APT::Periodic::AutocleanInterval "7";
APT::Periodic::Unattended-Upgrade "1";
EOF

# Configure updates.
cat << EOF > /etc/apt/apt.conf.d/50unattended-upgrades 
Unattended-Upgrade::Allowed-Origins {
    "${distro_id} ${distro_codename}-security";
    "${distro_id} ${distro_codename}-updates";
};
EOF
