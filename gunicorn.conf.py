# gunicorn.conf.py  

timeout = 1000

# 绑定到的IP地址和端口号  
bind = "0.0.0.0:8800"

# 日志配置  
loglevel = "debug"  
errorlog = "-"
accesslog = "-"