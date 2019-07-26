#!/bin/bash

function __yaml2json() { 
  ruby -ryaml -rjson -e 'puts JSON.pretty_generate(YAML.load(ARGF))' $*
}

export ADMINPASS="$(cat src/etc/config.yaml | __yaml2json | jq -r '.rabbitmq | .password')"
export WORKERPASS="$(cat src/etc/config.yaml | __yaml2json | jq -r '.rabbitmq | .worker')"

envsubst < docker-compose.yml.sample > docker-compose.yml

function build(){
  rm -Rf oauth-proxy 2>/dev/null
  git clone https://github.com/distributedportscan/oauth-proxy.git && cd oauth-proxy
  cd nginx && docker build -t nginx-authenticator . && cd ..
  cd ..
  rm -Rf oauth-proxy 2>/dev/null
  cd src && sudo docker build -t ds-manager . && cd ../
}

function start(){
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
