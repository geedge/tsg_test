#!/bin/sh

cd /opt/tsg_test/
docker build -t test:test .
sleep 15

docker run -d --name automation --privileged=true -p 8800:8800 test:test
# docker exec -it -uroot automation bash -c "java -jar /app/package/selenium-server-4.8.1.jar standalone &"
# docker exec -it -uroot automation bash -c "gunicorn -c gunicorn.conf.py app:app &"