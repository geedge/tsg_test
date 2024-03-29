# 从https://hub.docker.com/_/centos/tags 找到合适的镜像，docker name统一为package:base
FROM centos:7.9.2009

# 设置工作目录为/
WORKDIR /package_base

# 将当前目录内容复制到容器的/内
COPY . /package_base

# 安装基础包
RUN yum clean all && yum makecache
RUN yum -y update
RUN yum install -y net-tools wget unzip
RUN yum install -y epel-release zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc make
RUN yum install -y python3-devel java-1.8.0-openjdk
RUN yum install -y python3 python3-pip

# 通过pip3安装需要的包
RUN pip3 install --no-cache-dir -r requirements.txt

# 安装chrome和chromedriver
RUN chmod 777 ./*.py
RUN python3 install_chrome.py
