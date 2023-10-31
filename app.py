import requests
from config import USERS, ADMIN_UID, WX_APP_TOKEN, TASK_NAME
import json
from apscheduler.schedulers.blocking import BlockingScheduler
from wxpusher import WxPusher

# 设置API请求的URL
url = "https://api.v2.rainyun.com/user/reward/tasks"


# 签到单个账号
def sign_in_one(user):
	headers = {
		'x-api-key': user['x-api-key'],
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 '
		              'Safari/537.36',
		'Content-Type': 'application/json'
	}

	# 设置任务名称
	payload = {
		"task_name": TASK_NAME
	}

	# 将payload转换为JSON字符串
	data = json.dumps(payload)

	response = requests.post(url, headers=headers, data=data)

	status = ('雨云账号:' + user['remark'] + '，签到结果：') + json.dumps(response.json(), ensure_ascii=False)
	# send_wxpusher_message(user['notification_uid'], status)  # 我自用默认通知管理员
	return status


def sign_in_all():
	# 签到所有账号
	results = [sign_in_one(user) for user in USERS]
	return results


def send_wxpusher_message(uid, message):
	# 发送WxPusher消息
	WxPusher.send_message(message, uids=[uid], token=WX_APP_TOKEN)


# 定时任务
scheduler = BlockingScheduler()


@scheduler.scheduled_job("cron", hour="8", minute="10")
def timed_job():
	results = sign_in_all()
	# 组合所有账号的签到结果
	message = "\n".join(results)
	send_wxpusher_message(ADMIN_UID, message)  # 默认通知管理员


# 在定时任务开始之前立即执行一次
timed_job()

# 开始定时任务
scheduler.start()
