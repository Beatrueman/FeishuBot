# -*- coding: UTF-8 -*-
import requests
from requests_toolbelt import MultipartEncoder

#获取tenant_access_token
url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
post_data = {"app_id":"",
             "app_secret":""}
r = requests.post(url, data=post_data)
tat = r.json()["tenant_access_token"]

def uploadimage():
    url = "https://open.feishu.cn/open-apis/im/v1/images"
    form = {'image_type':'message','image':(open(r'','rb'))} #rb表示用二进制模式只读图片，open后填写图片路径
    multi_form = MultipartEncoder(form)
    headers = {
        'Authorization': 'Bearer '+tat #获取tenant_access_token
    }
    headers['Content-Type'] = multi_form.content_type
    response = requests.request("POST", url, headers=headers, data=form)
    print(response.content)

if __name__ == '__main__':
    uploadimage()
