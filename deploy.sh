#!/bin/bash

function __yaml2json() { 
  ruby -ryaml -rjson -e 'puts JSON.pretty_generate(YAML.load(ARGF))' $*
}

export ADMINPASS="$(cat src/etc/config.yaml | __yaml2json | jq -r '.rabbitmq | .password')"
export WORKERPASS="$(cat src/etc/config.yaml | __yaml2json | jq -r '.rabbitmq | .worker')"

envsubst < docker-compose.yml.sample > docker-compose.yml

function start(){
  cd src && sudo docker build -t ds-manager . && cd ../
  sudo docker-compose up -d
  sleep 5
  sudo docker exec -it rabbitmq rabbitmqctl add_user worker "$WORKERPASS"
  sudo docker exec -it rabbitmq rabbitmqctl set_permissions -p portscan worker ".*" ".*" ".*";
}

function stop(){
  sudo docker-compose down
}

function ps(){
  sudo docker-compose ps
}

$1
rm docker-compose.yml
