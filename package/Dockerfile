# 从https://hub.docker.com/_/centos/tags 找到合适的镜像，docker name统一为package:base
FROM rockylinux:9

# 设置工作目录为/
WORKDIR /package_base

# 将当前目录内容复制到容器的/内
COPY . /package_base

# 更改rockylink镜像源
# COPY ./rocky.repo /etc/yum.repos.d/rocky.repo
# COPY ./rocky-extras.repo /etc/yum.repos.d/rocky-extras.repo

# 安装基础包
RUN yum clean all && yum makecache
RUN yum -y update
RUN yum install -y net-tools wget unzip iproute
RUN yum install -y epel-release zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc make
RUN yum install -y python3-devel java-1.8.0-openjdk
RUN yum install -y python3 python3-pip
RUN yum install -y tcpdump pciutils bind-utils
RUN yum install -y kernel-devel kernel-headers
RUN yum install -y libffi-devel hping3
RUN yum group install -y "Development tools"
RUN yum install -y tcpreplay

RUN find . -type f -name "*.py" -exec chmod 777 {} \;

# 安装最新的python并修改软连接
RUN python3 install_python.py

# 通过pip3安装需要的包
RUN pip3 install --no-cache-dir -r requirements.txt

# 安装chrome和chromedriver
RUN python3 install_chrome.py

# 安装trex
RUN python3 install_trex.py

# 更新tsg_ca
RUN python3 update_tsg_ca.py

# 安装go并设置环境变量，可通过GO_VERSION动态修改版本号
RUN python3 install_go.py
# ENV GO_VERSION 1.23.2
# RUN wget https://golang.google.cn/dl/go${GO_VERSION}.linux-amd64.tar.gz | \
#     tar -C /usr/local -xzf go${GO_VERSION}.linux-amd64.tar.gz && \
RUN ln -s /usr/local/go/bin/go /usr/local/bin/go && \
    ln -s /usr/local/go/bin/godoc /usr/local/bin/godoc && \
    ln -s /usr/local/go/bin/gofmt /usr/local/bin/gofmt
ENV GOPATH /go
ENV PATH /usr/local/go/bin:${GOPATH}/bin:${PATH}
RUN mkdir -p ${GOPATH}/src ${GOPATH}/bin ${GOPATH}/pkg
