#!/bin/bash

# TODO: use code from deploy.sh 

YELLOW='\033[1;33m'
RESET='\033[0m'

echo -e "${YELLOW}Generating virtualenv...${RESET}"
source `which virtualenvwrapper.sh`
mkvirtualenv url -a . --python=/usr/bin/python3.4

echo -e "${YELLOW}Installing requirements...${RESET}"
pip3 install -r requirements.txt

echo -e "${YELLOW}Building docker - development environment...${RESET}"
cd docker/development
sudo docker-compose build

echo -e "${YELLOW}Running url-shortener server and mongodb in detached mode...${RESET}"
sudo docker-compose up -d

echo -e "${YELLOW}Running unit tests!${RESET}"
cdproject
python3 -m pytest