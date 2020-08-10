# Author: Xianghui Cui (github.com/iwillsky)
# Aug 01, 2020
# Install components on ParallelCluster AMI by steps

#!/bin/bash

### Install docker ###
sudo apt install -y docker.io
sudo usermod -aG docker $USER
newgrp docker

### Install nvidia-docker ###
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker

### Install boto3 & nvidia-ml
sudo python -m pip install --upgrade pip
sudo pip install boto3
sudo pip install nvidia-ml-py3

### Update & clean ###
sudo apt update
sudo apt upgrade

#Install FSx-Lustre client
wget -O - https://fsx-lustre-client-repo-public-keys.s3.amazonaws.com/fsx-ubuntu-public-key.asc | sudo apt-key add -
sudo bash -c 'echo "deb https://fsx-lustre-client-repo.s3.amazonaws.com/ubuntu bionic main" > /etc/apt/sources.list.d/fsxlustreclientrepo.list && apt-get update'
sudo apt install -y lustre-client-modules-$(uname -r)

### Self-test ###
docker run --gpus all nvidia/cuda:10.0-base nvidia-smi
