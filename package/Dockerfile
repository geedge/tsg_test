# 从https://hub.docker.com/_/centos/tags 找到合适的镜像，docker name统一为package:base
FROM rockylinux:8

# 设置工作目录为/
WORKDIR /package_base

# 将当前目录内容复制到容器的/内
COPY . /package_base

# 安装基础包
RUN yum clean all && yum makecache
RUN yum -y update
RUN yum install -y net-tools wget unzip iproute
RUN yum install -y epel-release zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc make
RUN yum install -y python3-devel java-1.8.0-openjdk
RUN yum install -y python3 python3-pip
RUN yum install -y tcpdump pciutils bind-utils curl
RUN yum install -y kernel-devel kernel-headers
RUN yum install -y libffi-devel
RUN yum group install -y "Development tools"

RUN find . -type f -name "*.py" -exec chmod 777 {} \;

# 安装python3.12
RUN python3 install_python.py

# 通过pip3安装需要的包
RUN pip3.12 install --no-cache-dir -r requirements.txt

# 安装chrome和chromedriver
RUN python3.12 install_chrome.py
RUN python3.12 install_trex.py
RUN python3.12 update_tsg_ca.py
