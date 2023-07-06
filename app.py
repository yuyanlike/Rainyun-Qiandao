import os
import requests
import json
import random
import smtplib
from email.mime.text import MIMEText
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取 API Key、备注和通知邮箱的列表
api_keys = os.getenv("API_KEYS").split(",")
remarks = os.getenv("API_KEY_REMARKS").split(",")
notification_emails = os.getenv("NOTIFICATION_EMAILS").split(",")

# 设置 API 请求的 URL
url = os.getenv("API_URL")

# 设置 SMTP 服务器和邮箱相关信息
smtp_server = os.getenv("SMTP_SERVER")
smtp_port = int(os.getenv("SMTP_PORT"))
smtp_username = os.getenv("SMTP_USERNAME")
smtp_password = os.getenv("SMTP_PASSWORD")
sender_email = os.getenv("SENDER_EMAIL")

# 设置 Headers
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

# 执行签到任务
def perform_sign_in(api_key, remark, notification_email):
    headers['x-api-key'] = api_key
    task_name = "每日签到"
    payload = {
        "task_name": task_name
    }
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()

    if response.status_code == 200:
        print(f"备注: {remark} - 签到成功")
        send_email(notification_email, remark, result)
    else:
        print(f"备注: {remark} - 签到失败，错误信息: {result['message']}")
        send_email(notification_email, remark, result)

# 发送邮件通知
def send_email(notification_email, remark, result):
    try:
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        smtp.starttls()
        smtp.login(smtp_username, smtp_password)
        email_content = create_email_content(remark, result)
        smtp.sendmail(sender_email, notification_email, email_content.as_string())
        print("邮件通知已发送")
    except Exception as e:
        print("发送邮件通知时出错:", str(e))
    finally:
        if 'smtp' in locals():
            smtp.quit()

# 遍历所有 API Key 签到
def sign_in_all():
    for i, api_key in enumerate(api_keys):
        if i < len(remarks) and i < len(notification_emails):
            remark = remarks[i]
            notification_email = notification_emails[i]
            perform_sign_in(api_key, remark, notification_email)
        else:
            print(f"API Key: {api_key} - 未设置备注或通知邮箱")

# 启动立刻执行一次
sign_in_all()

# 定时任务
scheduler = BlockingScheduler()
scheduler.add_job(sign_in_all, 'cron', hour='0-10', minute='0-59')
scheduler.start()
