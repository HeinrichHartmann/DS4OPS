# Update system
sudo apt-get -y update
sudo apt-get -y upgrade

# Install docker
curl -fsSL get.docker.com -o get-docker.sh
sh get-docker.sh
sudo usermod -aG docker ubuntu
