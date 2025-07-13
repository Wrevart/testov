#!/bin/bash
set -e

IMAGE_NAME=log_parser_image
CONTAINER_NAME=log_parser_container

docker build -t $IMAGE_NAME .

mkdir -p ./stats
mkdir -p ./config

if [ $(docker ps -aq -f name=$CONTAINER_NAME) ]; then
    docker rm -f $CONTAINER_NAME
fi

docker run -d \
  --name $CONTAINER_NAME \
  --memory=512m \
  --cpus=1 \
  --restart=on-failure:3 \
  -v /var/log/app:/var/log/app \
  -v $(pwd)/stats:/stats \
  -v $(pwd)/config:/app/config \
  $IMAGE_NAME 
