#!/bin/sh

chmod 777 /opt/tsg_test/app.py
chmod 777 /opt/tsg_test/gunicorn.conf.py
chmod 777 /opt/tsg_test/supervisor.conf
chmod 777 /opt/tsg_test/package/install_chrome.py
chmod 777 /opt/tsg_test/package/install_trex.py
chmod 777 /opt/tsg_test/package/requirements.txt

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

docker run -d --name automation --privileged -p 8800:8800 test:test
# docker exec -it -uroot automation bash -c "java -jar /app/package/selenium-server-4.8.1.jar standalone &"
# docker exec -it -uroot automation bash -c "gunicorn -c gunicorn.conf.py app:app &"
# ps -ef | grep selenium
# ps -ef | grep gunicorn
