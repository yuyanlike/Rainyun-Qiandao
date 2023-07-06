import os
import requests
import json
import smtplib
from email.mime.text import MIMEText
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()
# 获取用户ID、密码和API Key的列表
user_ids = os.getenv("USER_ID").split(",")
user_passwords = os.getenv("USER_PASSWORD").split(",")
api_keys = os.getenv("API_KEYS").split(",")
api_key_remarks = os.getenv("API_KEY_REMARKS").split(",")
# 设置API请求的URL
url = "https://api.v2.rainyun.com"
# 设置SMTP服务器和邮箱相关信息
smtp_server = os.getenv("SMTP_SERVER")
smtp_port = int(os.getenv("SMTP_PORT"))
smtp_username = os.getenv("SMTP_USERNAME")
smtp_password = os.getenv("SMTP_PASSWORD")
sender_email = os.getenv("SENDER_EMAIL")
# 设置Headers
headers = {
    'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
    'Content-Type': 'application/json'
}
# 创建邮件内容
def create_email_content(remark, result):
    subject = f"雨云签到结果 - {remark}"
    content = f"签到结果: {result}"
    email_content = MIMEText(content, 'plain')
    email_content['Subject'] = subject
    email_content['From'] = sender_email
    return email_content

# 执行登录操作
def perform_login(user_id, user_password, remark):
    payload = {
        "field": user_id,
        "password": user_password
    }
    response = requests.post(f"{url}/user/login", headers=headers, json=payload)
    result = response.json()
    if response.status_code == 200:
        return result["x-api-key"]
    else:
        print(f"用户ID: {user_id} -备注：{remark} - 登录失败，错误信息: {result['message']}")
        send_email(os.getenv("NOTIFICATION_EMAILS").split(",")[user_ids.index(user_id)], f"用户ID: {user_id}", f"备注：{remark}", result)
        return None

# 执行签到任务
def perform_sign_in(api_key, remark, notification_email, user_id):
    headers['x-api-key'] = api_key
    task_name = os.getenv("TASK_NAME")
    payload = {
        "task_name": task_name
    }
    response = requests.post(f"{url}/user/reward/tasks", headers=headers, json=payload)
    result = response.json()

    if response.status_code == 200:
        print(f"备注: {remark} - 用户id：{user_id} - 签到成功")
        send_email(notification_email, remark, result, user_id)
    else:
        print(f"备注: {remark} - 用户id：{user_id} - 签到失败，错误信息: {result['message']}")
        send_email(notification_email, remark, result, user_id)  
# 发送邮件通知
def send_email(notification_email, remark, result, user_id):
    try:
        smtp = smtplib.SMTP_SSL(smtp_server, smtp_port)  
        smtp.login(smtp_username, smtp_password)
        email_content = create_email_content(remark, result)
        smtp.sendmail(sender_email, notification_email, email_content.as_string())
        print(f"邮件通知已发送 - 用户ID: {user_id} - 邮件地址: {notification_email}")
    except Exception as e:
        print(f"发送邮件通知时出错: {str(e)} - 用户ID: {user_id} - 邮件地址: {notification_email}")
    finally:
        if 'smtp' in locals():
            smtp.quit()


# 遍历所有账号登录并签到
def sign_in_all():
    for index, (user_id, user_password) in enumerate(zip(user_ids, user_passwords)):
        if user_id in user_ids and api_keys[user_ids.index(user_id)]:
            remark = api_key_remarks[user_ids.index(user_id)] 
            notification_email = os.getenv("NOTIFICATION_EMAILS").split(",")[index] if index < len(os.getenv("NOTIFICATION_EMAILS").split(",")) else None
            api_key = api_keys[user_ids.index(user_id)]
            if api_key:
                perform_sign_in(api_key, remark, notification_email, user_id)  
        else:
            print(f"用户ID: {user_id} - 未设置API Key")

# 启动立即执行一次
sign_in_all()

# 定时任务
scheduler = BlockingScheduler()
scheduler.add_job(sign_in_all, 'cron', hour=8, minute=0)  # 每天的8:00 AM触发签到任务
scheduler.start()
