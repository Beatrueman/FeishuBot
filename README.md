# 飞书机器人

## 更新与修复

### 2023年8月28日更新

1.将原先的`TestApi.py`整合进`ChatApi.py`中，省去了繁琐的目录与代码文件

2.更新了请求地址配置方法，只需要一个文件`ChatApi.py`即可

## **飞书机器人介绍**

> [机器人概述 - 开发指南 - 开发文档 - 飞书开放平台 (feishu.cn)](https://open.feishu.cn/document/client-docs/bot-v3/bot-overview)

飞书机器人分为两种，一种是**自定义机器人**，一种是**应用机器人**。

### 自定义机器人

只能在群聊中使用，只能完成比较固定的消息推送。

***webhook*获取方法：**

1.进入目标群组，在群组右上角点击更多按钮，并点击 **设置**。

![img](https://sf3-cn.feishucdn.com/obj/open-platform-opendoc/3717a10d5e293fc80d296267478f4bb3_LREe0920Bf.png?height=1524&lazyload=true&maxWidth=600&width=2020)

2.在右侧 **设置** 界面，点击 **群机器人**。

![img](https://gitee.com/beatrueman/images/raw/master/img/202307311837969.png)

3.在 **群机器人** 界面点击 **添加机器人**。

4.在 **添加机器人** 对话框，找到 **自定义机器人**，并 **添加**。

![img](https://gitee.com/beatrueman/images/raw/master/img/202307311838153.png)

5.设置自定义机器人的名称与描述，并点击 **添加**。

![img](https://gitee.com/beatrueman/images/raw/master/img/202307311838285.png)

6.获取自定义机器人的 *webhook* 地址，并点击 **完成**

![img](https://gitee.com/beatrueman/images/raw/master/img/202307311840164.png)

### 应用机器人

功能很多，开发性高，灵活性强。需要有企业账户，支持对话互动等多种功能。

#### *app_id*与*app_secret*获取方法

1.用企业账户，在开发者后台中，**创建企业自建应用**

![image-20230731184331697](https://gitee.com/beatrueman/images/raw/master/img/202307311843815.png)

2.找到app_id与qpp_secret

![image-20230731184507412](https://gitee.com/beatrueman/images/raw/master/img/202307311845488.png)

3.添加应用能力，选择机器人

![image-20230731184549009](https://gitee.com/beatrueman/images/raw/master/img/202307311845159.png)

4.添加以下权限

```
im:message,im:message.group_at_msg,im:message.group_at_msg:readonly,im:message.group_msg,im:message.p2p_msg,im:message.p2p_msg:readonly,im:message:readonly,im:chat:readonly,im:chat,im:message:send_as_bot
```

![image-20230731184637236](https://gitee.com/beatrueman/images/raw/master/img/202307311846289.png)

开启***事件订阅***：

若要使机器人有互动对话功能，需要填写请求配置地址，并添加**接收消息v2.0**和**消息已读v2.0**事件

![image-20230802165643614](https://gitee.com/beatrueman/images/raw/master/img/202308021656698.png)

#### **请求地址配置**方法

**1.使用反向代理工具ngrok完成内网穿透**

使用docker启动ngrok

```
docker run -it -e NGROK_AUTHTOKEN=<token> ngrok/ngrok http 8080
```

***NGROK_AUTHTOKEN***获取方法：

1.1 进入ngrok官网[https://ngrok.com/](https://link.zhihu.com/?target=https%3A//ngrok.com/)，注册ngrok账号并下载ngrok

1.2 获取Authtoken

![image-20230803123131090](https://gitee.com/beatrueman/images/raw/master/img/202308031231178.png)

获取公网地址后，按下Ctrl + P，然后再按下Ctrl + Q，使容器后台运行。

![image-20230803123606894](https://gitee.com/beatrueman/images/raw/master/img/202308031236943.png)

1.3 在`FeishuBot/public/chat/conf.py`中填写相关信息

先运行`ChatApi.py`

```
python3 ChatApi.py
```

到飞书后台填写请求配置地址，格式为https://123456.ngrok-free.app/query/message

期间保证ngrok在后台一直运行

**2.使用Kubernetes暴露公网**

2.1 在`FeishuBot/public/build-api`填好`conf.py`中的信息，然后自己制作docker镜像

```
docker build -t docker的用户名/镜像名:<tag> .
docker push 做好的镜像
```

2.2在`FeishuBot/public/build-api`下，修改`deploy.yaml`

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  replicas: 1
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
      - name: api
        image:  # 在build-api目录下制作的镜像
        ports:
        - containerPort: 8080

---
apiVersion: v1
kind: Service
metadata:
  name: api
spec:
  selector:
    app: api
  type: NodePort
  ports:
  - name: http  
    protocol: TCP
    port: 80  # 对外暴露的端口
    targetPort: 8080 # Flask应用容器监听的端口
    nodePort: 39378

```

然后获取检验用的请求配置地址

```
kubectl apply -f deploy.yaml
kubectl get svc # 获取端口为39378,记得在服务器开放
```

地址示例：http://1.2.3.4:3XXXXX/query/message

![image-20230803185245586](https://gitee.com/beatrueman/images/raw/master/img/202308031852674.png)

## **功能**

* 青年大学习提醒
* 天气通知
* 互动对话功能
* ChatGPT—引用网上项目

### 青年大学习提醒

实现每周一早上九点，通知用户完成青年大学习

点击超链接跳转微信

![image-20230731180846759](https://gitee.com/beatrueman/images/raw/master/img/202307311808856.png)

使用方法

**自定义机器人**：在`FeishuBot/personal/conf.py`中填写你的webhook

**应用机器人**：在`FeishuBot/public/send/conf.py`中填写你的app_id和app_secret

开启服务：自定义机器人启动脚本`FeishuBot/personal/qndxx-remind/run1.sh`

​                    应用机器人启动脚本`FeishuBot/public/send/qndxx-remind/run1.sh`

```
chmod +x run1.sh
./run1.sh
```

### 天气通知

实现每天早上七点，向用户推送天气信息

普通天气

![image-20230731190241182](https://gitee.com/beatrueman/images/raw/master/img/202307311902236.png)

出现灾害天气时，推送气象台预警信息，并附带特殊天气图标

![image-20230731190331070](https://gitee.com/beatrueman/images/raw/master/img/202307311903116.png)

使用方法

**自定义机器人**：在`FeishuBot/personal/conf.py`中填写你的webhook和指定城市

**应用机器人**：在`FeishuBot/public/send/conf.py`中填写你的app_id和app_secret，指定城市

开启服务：自定义机器人启动脚本`FeishuBot/personal/weather-remind/run2.sh`

​                    应用机器人启动脚本`FeishuBot/public/send/weather-remind/run2.sh`

```
chmod +x run1.sh
./run2.sh
```

### 互动对话功能

**仅限应用机器人**

**互动对话逻辑**

![img](https://gitee.com/beatrueman/images/raw/master/img/202308032313540.jpeg)

实现向应用机器人发送特定信息，返回特定内容

1.用户发送”**青年大学习**“，机器人回复青年大学习通知内容

![image-20230801223157822](https://gitee.com/beatrueman/images/raw/master/img/202308012231904.png)

2.用户发送"**查询天气：指定城市名**"后，机器人回复需要监测天气城市的天气信息。

城市名注意不要带市和区。 如: 北京、南岸

![image-20230802110517854](https://gitee.com/beatrueman/images/raw/master/img/202308021105899.png)

![image-20230802120451729](https://gitee.com/beatrueman/images/raw/master/img/202308021204780.png)

### ChatGPT

参考网上的项目，建议使用新的应用机器人

> [飞书 ChatGPT 机器人 - 用 JavaScript 五分钟开发一个飞书 ChatGPT 机器人 (aircode.cool)](https://aircode.cool/q4y1msdim4)

## BUG

~~1.用K8s配置请求地址时，用于检验时地址都是可用的，但是更改镜像后，无法使用互动对话功能~~

2.互动对话功能在服务器上使用ngrok有点问题，在windows下完全可以使用

~~3.因为配置请求地址时需要在固定地址的情况下改变镜像，所以GitLab中的CI只跑通用于检验的镜像并部署在K8s，详情请看.gitlab-ci.yaml~~

![image-20230804185615165](https://gitee.com/beatrueman/images/raw/master/img/202308041856285.png)
