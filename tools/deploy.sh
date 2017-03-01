#!/bin/bash

USER=$1
HOST=$2

YELLOW='\033[1;33m'
RESET='\033[0m'

function cecho {
    echo -e "${YELLOW}$1${RESET}"
}

function update_source_code {
    cecho "Updating source code..."
    ssh ${USER}@${HOST} /bin/bash << EOF
    if [ ! -d url-shortener ]; then
      git clone https://github.com/bblazej92/url-shortener.git
    fi
    cd url-shortener
    git fetch -p
    git reset --hard origin/master
EOF
}

function update_virtualenv {
    cecho "Updating virtualenv..."
    ssh ${USER}@${HOST} /bin/bash << EOF
    if [ ! -d ~/.virtualenvs/shortener ]; then
        echo "Installing virtualenv shortener..."
        export LC_ALL=C.UTF-8
        export LANG=C.UTF-8
        sudo apt-get update
        sudo apt-get install -y python-pip
        sudo pip install virtualenv
        sudo pip install virtualenvwrapper
        source `which virtualenvwrapper.sh`
        mkvirtualenv --python=/usr/bin/python3 -a url-shortener shortener
        sudo apt-get install -y python3-pip
    else
        source `which virtualenvwrapper.sh`
    fi
    workon shortener
    pip install -r requirements.txt
EOF
}

function update_docker_images {
    cecho "Updating docker images..."
    ssh ${USER}@${HOST} /bin/bash << EOF
    source /home/${USER}/.profile
    `hash docker-compose > /dev/null 2>&1`
    if [ $? -eq 1 ]; then
        export LC_ALL=C.UTF-8
        export LANG=C.UTF-8
        echo "Installing docker-compose..."
        pip install docker-compose==1.8.0
    fi
    cd url-shortener/docker/production
    hash=`head /dev/urandom | tr -dc A-Za-z0-9 | head -c 13 ; echo ''`
    sed -e 's/!HASH!/${hash}/g'
    docker-compose build
EOF
}

function restart_production {
    cecho "Restarting production..."
    ssh ${USER}@${HOST} /bin/bash << EOF
    source /home/${USER}/.profile
    cd url-shortener/docker/production
    docker-compose up -d
EOF
}


function deploy {
    cecho "Deploying new version of code..."
    update_source_code
    update_virtualenv
    update_docker_images
    restart_production
}


# RUN DEPLOYMENT
deploy
