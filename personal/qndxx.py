# -*- coding: UTF-8 -*-
import json
import requests
import conf

# webhook地址
webhook_url = conf.WEBHOOK_URL

payload_message = {
        "msg_type": "post", #msg_type值为对应消息类型的映射关系
        "content": { #content包含消息内容
                "post": {
                        "zh_cn": {
                                "title": "青年大学习通知",
                                "content": [
                                        [{
                                                        "tag": "at", #@标签
                                                        "user_id": "all"
                                                },
                                                {
                                                        "tag": "text", #文本标签
                                                        "text": "记得做青年大学习哦"
                                                }
                                        ],
                                        [
                                                {
                                                         "tag": "a", #超链接标签                                                      
                                                         "text": "点击转到重庆共青团微信公众号",
                                                         "href": "http://qndxx.cqyouths.com"
                                                },
                                                {
                                                         "tag": "img",
                                                         "image_key": "img_v2_411c591f-d263-4843-912c-f7fb637549bg"
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

