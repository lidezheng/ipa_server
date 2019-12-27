#!/bin/bash
# Nginx日志按照天级切分
logs_path="/var/log/nginx/"
pid_path="/usr/local/nginx/logs/nginx.pid"
DATE=`date -d "yesterday" +"%Y%m%d"`
mv ${logs_path}access.log ${logs_path}access_${DATE}.log
gzip ${logs_path}access_${DATE}.log
kill -USR1 `cat ${pid_path}`
