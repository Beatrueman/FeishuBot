# -*- coding: UTF-8 -*-
import requests
from requests_toolbelt import MultipartEncoder

#获取tenant_access_token
url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
post_data = {"app_id":"cli_a42011585561100d",
             "app_secret":"AYRFbDlUH8OKxRweuXM47cLLFwRpO12X"}
r = requests.post(url, data=post_data)
tat = r.json()["tenant_access_token"]

def uploadimage():
    url = "https://open.feishu.cn/open-apis/im/v1/images"
    form = {'image_type':'message','image':(open(r'C:\Users\李逸雄\Desktop\寒潮.png','rb'))} #rb表示用二进制模式只读图片
    multi_form = MultipartEncoder(form)
    headers = {
        'Authorization': 'Bearer '+tat #获取tenant_access_token
    }
    headers['Content-Type'] = multi_form.content_type
    response = requests.request("POST", url, headers=headers, data=multi_form)
    print(response.content)

if __name__ == '__main__':
    uploadimage()
