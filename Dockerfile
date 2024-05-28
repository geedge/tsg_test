FROM package:base

# 设置工作目录为/app
WORKDIR /app

# 将当前目录内容复制到容器的/app内
COPY . /app

# 赋权限
# RUN chmod 777 ./*.py
RUN find . -type f -name "*.py" -exec chmod 777 {} \;

# 创建supervisord.log文件
RUN touch /var/log/supervisord.log
RUN touch /var/log/selenium_stdout.log
RUN touch /var/log/selenium_stderr.log
RUN touch /var/log/gunicorn_stdout.log
RUN touch /var/log/gunicorn_stderr.log

# 对外暴露的端口号
EXPOSE 8800

# 当容器启动时运行supervisor，用于启动selenium server和flask server
CMD ["/usr/local/bin/supervisord", "-c", "/app/supervisor.conf"]
# CMD ["tail", "-f", "/dev/null"]
