FROM package:base

# 设置工作目录为/app
WORKDIR /app

# 将当前目录内容复制到容器的/app内
COPY . /app

# 赋权限
RUN chmod 777 ./*.py

# 对外暴露的端口号
EXPOSE 8800

# 当容器启动时运行python脚本
CMD ["/usr/local/bin/supervisord", "-c", "/app/supervisor.conf"]
# CMD ["tail", "-f", "/dev/null"]