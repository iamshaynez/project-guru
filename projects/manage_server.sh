#!/bin/bash

# 定义项目的路径
PROJECT_DIR="/path/to/your/django/project"
# 定义日志文件的路径
LOG_FILE="runserver.log"

# 进入项目目录
cd $PROJECT_DIR

# 启动或停止 Django 开发服务器
case "$1" in
  start)
    echo "Starting Django development server."
    # 使用 nohup 和 & 在后台运行服务器，输出会被重定向到日志文件
    nohup python manage.py runserver 0.0.0.0:8000 > $LOG_FILE 2>&1 &
    echo $! > runserver.pid
    ;;
  stop)
    echo "Stopping Django development server."
    # 读取服务器进程的 PID 并杀掉它
    if [ -f runserver.pid ]; then
      kill $(cat runserver.pid)
      rm runserver.pid
    else
      echo "PID file not found. Can't stop server."
    fi
    ;;
  *)
    echo "Usage: $0 {start|stop}"
    exit 1
esac