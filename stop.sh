#!/bin/sh

docker stop $(docker ps -aq)
sleep 10
docker rm $(docker ps -aq)

docker rmi test:test
# docker rmi $(docker images -q)

docker ps -a
docker images
