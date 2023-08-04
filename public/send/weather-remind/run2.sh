#!/bin/sh

echo "开始配置服务......"

chmod +x /root/FeishuBot/public/send/weather.py

mv weather.service /etc/systemd/system/
mv weather.timer /etc/systemd/system/
cd /etc/systemd/system/
sudo systemctl enable weather.service
sudo systemctl start weather.service

echo "查看服务是否启动......"

sudo systemctl status weather.service

echo "开始配置定时服务......"
echo "定时器将在每天的早上 7 点触发."

sudo systemctl enable weather.timer
sudo systemctl start weather.timer

echo "查看定时任务是否启动......"

sudo systemctl status weather.timer

echo "若均为active则成功"