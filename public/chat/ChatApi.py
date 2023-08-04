import logging
from queue import Queue
from flask import Flask, request, jsonify, json
import requests
import conf

app = Flask(__name__) # 创建Flask应用程序
consumer = Queue() # 创建队列用于存储接收到的消息
logging.basicConfig(level=logging.INFO) # 设置日志级别为INFO,用于输出日志信息
sent_cities = set() # 记录已发送过天气信息的城市

class FeishuResponse:
    def __init__(self, messageId, query): # 初始化类时，需要传入messageId和query值
        self.messageId = messageId
        self.query = query

    def to_json(self): # 将Feishu消息的响应转化为JSON格式
        return {
            "messageId": self.messageId,
            "query": self.query
        }

@app.route('/query/message', methods=['POST']) # 添加路由处理函数,配置请求地址在/query/message下
def message(): # 用于处理来自飞书服务器的HTTP POST请求
    print("收到消息！")
    logging.info("收到飞书消息：%s", request.data) # 将飞书服务器发送的数据存储在日志中
    body = request.get_json() # 从HTTP请求中解析JSON,存储在body中
    header = body.get('header') # 提取header
    eventType = header.get('event_type') # 提取header中的event_type
    
    # 判断事件类型和消息类型
    if eventType == 'im.message.receive_v1':
        event = body.get('event') # body中提取的event表示事件具体内容
        message = event.get('message') # event中提取的message表示飞书收到用户的消息内容
        messageType = message.get('message_type') # message中提取message_type表示消息类型
        
        # 处理文本消息
        if messageType == 'text':
            messageId = message.get('message_id') # 表示飞书消息的唯一标识
            content = message.get('content') # 文本消息的内容
            contentJson = json.loads(content) # 解析出JSON格式的文本消息内容
            text = contentJson.get('text') # 表示文本消息的具体内容

            feishuResponse = FeishuResponse(messageId, text) # FeishuResponse对象将message_id和文本内容作为参数传入
            logging.info("投递用户消息：%s", feishuResponse.to_json()) # 将投递的用户消息的相关事件体信息记录到日志中
            consumer.put(feishuResponse)
            
            # 获取tenant_access_token
            url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
            post_data = {
                "app_id": conf.APP_ID,
                "app_secret": conf.APP_SECRET
            }
            r = requests.post(url, json=post_data)
            tat = r.json()["tenant_access_token"]
            
            #通过手机号或邮箱获取用户的open_id
            id_url = "https://open.feishu.cn/open-apis/contact/v3/users/batch_get_id?user_id_type=open_id"
            id_payload = {
                "mobiles": [conf.MOBILES] #用户注册飞书的手机号
            }
            id_data = requests.post(id_url, json=id_payload, headers={'Authorization': 'Bearer '+tat}).json()
            user_id = id_data['data']['user_list'][0]['user_id'] # [0]是一个索引，指定要访问的元素在user_list数组中的位置
            
            # 提取用户发送的信息
            receive_data = feishuResponse.to_json()
            receive_content = receive_data['query']

            
            # 如果用户发送的消息为“青年大学习”，则发送消息
            if receive_content == '青年大学习':
                url = "https://open.feishu.cn/open-apis/im/v1/messages"
                params = {"receive_id_type":"open_id"}
                msgContent = {
                    "zh_cn": {
                        "title": "青年大学习通知",
                        "content": [
                            [{
                                "tag": "at",
                                "user_id": "all"
                            },
                            {
                                "tag": "text",
                                "text": "记得做青年大学习哦"
                            }],
                            [
                                {
                                    "tag": "a",
                                    "text": "点击转到重庆共青团微信公众号",
                                    "href": "http://weixin.qq.com/r/lHWSl7LEVXopKPb0byAQ"
                                },
                                {
                                    "tag": "img",
                                    "image_key": "img_v2_411c591f-d263-4843-912c-f7fb637549bg"
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
                    'Authorization': 'Bearer '+tat,
                    'Content-Type': 'application/json'
                }
                requests.post(url, params=params, headers=headers, data=payload)
            
            if '查询天气' in receive_content:
                #分割用户发送的信息
                _,city = receive_content.split('：') # 通过冒号分隔字符串

                # 检查城市是否已经发送过天气信息，避免重复发送天气信息
                if city in sent_cities:
                    logging.info("城市 %s 天气信息已发送", city)
                else:
                    # 传入城市
                    weather_url = "https://v0.yiketianqi.com/api?unescape=1&version=v61&appid=75465165&appsecret=VLz7P9xd"
                    params = {"city": {city}}
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
                
                    # 发送天气预报
                    url = "https://open.feishu.cn/open-apis/im/v1/messages"
                    params = {"receive_id_type":"open_id"}
                    msgContent = {
                        "zh_cn": {
                            "title": "天气预报",
                            "content": [
                                [{
                                    "tag": "text",
                                    "text": text
                                }],
                                [
                                    {
                                        "tag": "a",
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
                        'Authorization': 'Bearer '+tat,
                        'Content-Type': 'application/json'
                    }
                    requests.post(url, params=params, headers=headers, data=payload)                


        else:
            logging.info("非文本消息")
            
    return jsonify(body)

if __name__ == "__main__":
    ngrok_url = conf.NGROK_URL
    app.run(host='0.0.0.0', port=5000)

