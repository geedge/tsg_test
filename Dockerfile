# 使用官方的Python运行时作为父镜像
FROM python:3.6.8

# 设置工作目录为/app
WORKDIR /opt/app

# 将当前目录内容复制到容器的/app内
# ADD . /app
COPY . .

# 赋权限
RUN chmod 777 ./*.py

# 通过yum安装需要的包
RUN python3 server/install_package.py

# 通过pip安装需要的包
RUN pip3 install --no-cache-dir -r requirements.txt

# 对外暴露的端口号
EXPOSE 8000

# 定义环境变量
ENV NAME World

# 当容器启动时运行python脚本
CMD ["python3", "tests/ui/security/security_rule_test.py"]