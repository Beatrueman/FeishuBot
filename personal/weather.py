# -*- coding: UTF-8 -*-
import requests
import json
import conf

weather_url = "https://v0.yiketianqi.com/api?unescape=1&version=v61&appid=75465165&appsecret=VLz7P9xd"
webhook_url = conf.WEBHOOK_URL
params = {
    "city": conf.CITY
}

response = requests.get(weather_url, params=params)
weather_data = response.json()

# 提取天气信息
weather_city = weather_data["city"]
wea = weather_data["wea"]
tem1 = weather_data["tem1"]
tem2 = weather_data["tem2"]
air_level = weather_data["air_level"]
air_tips = weather_data["air_tips"]
alarm_type = weather_data['alarm']['alarm_type']
alarm_content = weather_data['alarm']['alarm_content']

alarm = f'***天气预警***\n今天将会有{alarm_type},注意安全！\n***预警信息***\n{alarm_content}\n*************'
weather = f'城市:{weather_city}\n今天的天气:{wea}\n最高温度:{tem1}度\n最低温度:{tem2}度\n空气质量:{air_level}\n小贴士:{air_tips}\n'

# 天气预警分类
if alarm_type == '暴雨':
    text = alarm + '\n' + weather
    img_key = "img_v2_6354622b-c25d-4a2c-bc21-e69dbb546ccg"
elif alarm_type == '高温':
    text = f'***天气预警***\n今天将会有{alarm_type},注意避暑！\n***预警信息***\n{alarm_content}\n*************' + '\n' + weather
    img_key = "img_v2_d1ea8a3b-1c77-4c54-a0d8-1927387662ag"
elif alarm_type == '雷电':
    text = alarm + '\n' + weather
    img_key = "img_v2_2d00fb0f-c83a-437e-8865-a07a894d53bg"
elif alarm_type == '道路结冰':
    text = alarm + '\n' + weather
elif alarm_type == '台风':
    text = alarm + '\n' + weather
    img_key = "img_v2_e5f2e7fc-927c-4be8-85fa-33c3c02adefg"
elif alarm_type == '寒潮':
    text = f'***天气预警***\n今天将会有{alarm_type},注意保暖！\n***预警信息***\n{alarm_content}\n*************' + '\n' + weather
    img_key = "img_v2_9300a000-c5de-44b3-8385-25d938d6049g"
else:
    text = weather
    img_key = "img_v2_bbe85078-0a27-4b35-aded-b0908bc66c4g"

payload_message = {
        "msg_type": "post", #msg_type值为对应消息类型的映射关系
        "content": { #content包含消息内容
                "post": {
                        "zh_cn": {
                                "title": "天气预报",
                                "content": [
                                        [
                                                {
                                                        "tag": "text", #文本标签
                                                        "text": text
                                                }
                                        ],
                                        [
                                                {
                                                         "tag": "a", #超链接标签                                                      
                                                         "text": "详情请看中央气象台官网",
                                                         "href": "http://www.nmc.cn/"
                                                },
                                                {
                                                         "tag": "img",
                                                         "image_key": img_key
                                                }
                                        ]
                                ]
                        }
                }
        }
}

headers = {
    'Content-Type': 'application/json'
}

response = requests.request("POST", webhook_url, headers=headers, data=json.dumps(payload_message))

print(response.text)