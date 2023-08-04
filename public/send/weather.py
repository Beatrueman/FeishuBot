import json
import requests
import conf

# 获取tenant_access_token
url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
post_data = {"app_id": conf.APP_ID,
             "app_secret": conf.APP_SECRET}
r = requests.post(url, data=post_data)
tat = r.json()["tenant_access_token"]

# 通过手机号或邮箱获取用户的open_id
id_url = "https://open.feishu.cn/open-apis/contact/v3/users/batch_get_id?user_id_type=open_id"
id_payload = {
    "mobiles": [
        conf.MOBILES
    ]
}
id = json.dumps(id_payload)
headers = {
        'Authorization': 'Bearer '+tat, #tenant_access_token
        'Content-Type': 'application/json'
}

response = requests.request("POST", id_url, headers=headers, data=id)
id_data = response.json()
# 获取user_id
user_id = id_data['data']['user_list'][0]['user_id'] # [0]是一个索引，指定要访问的元素在user_list数组中的位置

# 调用天气api
weather_url = "https://v0.yiketianqi.com/api?unescape=1&version=v61&appid=75465165&appsecret=VLz7P9xd"

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

#发送消息
def send():
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    params = {"receive_id_type":"open_id"} #接收人的open_id
    msgContent = {
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
    
    req = {
        "receive_id": user_id, 
        "msg_type": "post",
        "content": json.dumps(msgContent)
    }
    payload = json.dumps(req)
    headers = {
        'Authorization': 'Bearer '+tat, #tenant_access_token
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, params=params, headers=headers, data=payload)
    print(response.content) 

if __name__ == '__main__':
    send()
