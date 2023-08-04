#!/bin/sh

echo "开始配置服务......"

chmod +x /root/FeishuBot/qndxx.py

mv qndxx.service /etc/systemd/system/
mv qndxx.timer /etc/systemd/system/
cd /etc/systemd/system/
sudo systemctl enable qndxx.service
sudo systemctl start qndxx.service

echo "查看服务是否启动......"

sudo systemctl status qndxx.service

echo "开始配置定时服务......"
echo "将在系统启动后的10分钟和每个星期一的早上9点启动青年大学习提醒服务。"

sudo systemctl enable qndxx.timer
sudo systemctl start qndxx.timer

echo "查看定时任务是否启动......"

sudo systemctl status qndxx.timer

echo "若均为active则成功"

