#!/bin/bash

function __yaml2json() { 
  ruby -ryaml -rjson -e 'puts JSON.pretty_generate(YAML.load(ARGF))' $*
}

export ADMINPASS="$(cat src/etc/config.yaml | __yaml2json | jq -r '.rabbitmq | .password')"
export WORKERPASS="$(cat src/etc/config.yaml | __yaml2json | jq -r '.rabbitmq | .worker')"

envsubst < docker-compose.yml.sample > docker-compose.yml

function build(){
  rm -Rf oauth-proxy 2>/dev/null
  git clone https://github.com/distributedportscan/oauth-proxy.git 
  docker build -t nginx-authenticator -f oauth-proxy/nginx/Dockerfile oauth-proxy/nginx/
  docker build -t authenticator -f oauth-proxy/app/Dockerfile oauth-proxy/app/
  rm -Rf oauth-proxy 2>/dev/null
  docker build -t ds-manager -f src/Dockerfile src/
}

function start(){
  docker-compose up -d
  sleep 5
  docker exec -it rabbitmq rabbitmqctl add_user worker "$WORKERPASS"
  docker exec -it rabbitmq rabbitmqctl set_permissions -p portscan worker ".*" ".*" ".*";
}

function stop(){
  docker-compose down
}

function ps(){
  docker-compose ps
}

$1
rm docker-compose.yml

