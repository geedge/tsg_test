#!/bin/sh

systemctl disable firewalld.service

cd /opt
git clone git@git.mesalab.cn:chongming/tsg_test.git
cd /opt/tsg_test
git checkout develop
find . -type f -name "*.py" -exec chmod 777 {} \;
chmod 777 /opt/tsg_test/supervisor.conf
chmod 777 /opt/tsg_test/package/requirements.txt
chmod 777 /opt/tsg_test/package/tsg_ca.txt
chmod 777 /etc/pki/tls/certs/ca-bundle.crt

python3 /opt/tsg_test/package/install_docker.py

if [[ "$(docker images -q)" == "" ]] || [[ "$(docker images --format "{{.Repository}}:{{.Tag}}" | grep 'package')" != "package:base" ]]; then
    echo "No Docker images, start to building."
    cd /opt/tsg_test/package/
    docker build -t package:base .
    echo "The Docker images have been created."
else
    echo "Exist Docker images"
fi

docker images

if [[ "$(docker ps -q)" == "" ]]; then
    echo "No Docker containers, start to building."
    cd /opt/tsg_test/
    docker build -t test:test .
    echo "The Docker containers have been created."
else
    echo "Exist Docker containers"
fi

docker ps -a

docker run -d --network=host --name automation --privileged --cap-add=ALL -v /dev:/dev -v /lib/modules:/lib/modules -p 8800:8800 test:test
