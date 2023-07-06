# 用户id,用逗号分隔
USER_ID=42701,4701,401
# 用户密码，用逗号分隔，顺序与用户id对应
USER_PASSWORD=123456,123456,123456
# API Keys，用逗号分隔，顺序与用户id对应
API_KEYS=MsuzDEkLelH2EJy1rua,MsuzDEkLelH2EJmyHNMrua,45641fsdfsageshADSDAS,45SDAS
# API Key 的备注，用逗号分隔，顺序与 API Keys 对应
API_KEY_REMARKS=Remark1,Remark2,Remark3,Remark4
# API Key 的通知邮箱，用逗号分隔，顺序与 API Keys 对应
NOTIFICATION_EMAILS=email1@example.com,email2@example.com,email3@example.com,email4@example.com

# 签到任务名称
TASK_NAME=每日签到


# 雨云接口URL
API_URL=https://api.v2.rainyun.com/

# 使用SMTP发送邮件，需要配置以下信息
# SMTP 服务器地址
SMTP_SERVER=your_smtp_server
# SMTP 服务器端口号
SMTP_PORT=587
# 邮箱用户名
SMTP_USERNAME=your_email@example.com
# 邮箱密码
SMTP_PASSWORD=your_email_password
# 发件人邮箱
SENDER_EMAIL=your_email@example.com


抱歉 以上的描述错误，雨云需要每天登录后才能签到 所以我们需要先登录然后签到。
下面是雨云的登录接口和签到接口。请你根据我们之前的聊天记录和代码  完成新的多账号的登录和签到代码。
# 登陆：
post 
https://api.v2.rainyun.com/user/login
请求参数
Header 参数
x-api-key string 全 必需
Body 参数 (application/json)
field string   必需   该参数在环境变量设置为 USER_ID
password string  必需  该参数在环境变量设置为 USER_PASSWORD
##示例代码：

import http.client
import json

conn = http.client.HTTPSConnection("api.v2.rainyun.com")
payload = ''
headers = {
   'x-api-key': '',
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
   'Content-Type': 'application/json'
}
conn.request("POST", "/user/login", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))

# 签到
post
https://api.v2.rainyun.com/user/reward/tasks
请求参数
Header 参数
x-api-key string 全 必需
Body 参数 (application/json)
task_name string   必需   该参数在环境变量设置为TASK_NAME
 ## 示例代码：

import http.client
import json

conn = http.client.HTTPSConnection("api.v2.rainyun.com")
payload = ''
headers = {
   'x-api-key': '',
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
   'Content-Type': 'application/json'
}
conn.request("POST", "/user/reward/tasks", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))


