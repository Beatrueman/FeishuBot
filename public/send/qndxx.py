import json
import requests
import conf

#获取tenant_access_token
url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
post_data = {"app_id": conf.APP_ID,
             "app_secret": conf.APP_SECRET}
r = requests.post(url, data=post_data)
tat = r.json()["tenant_access_token"]

#通过手机号或邮箱获取用户的open_id
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
user_id = id_data['data']['user_list'][0]['user_id'] #[0]是一个索引，指定要访问的元素在user_list数组中的位置

#发送消息
def send():
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    params = {"receive_id_type":"open_id"} #接收人的open_id
    msgContent = {
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
        'Authorization': 'Bearer '+tat, #tenant_access_token
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, params=params, headers=headers, data=payload)
    print(response.headers['X-Tt-Logid']) # for debug or oncall
    print(response.content) # Print Response

if __name__ == '__main__':
    send()
