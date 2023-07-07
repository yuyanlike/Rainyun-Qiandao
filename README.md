# 雨云签到

- 这是一个用于在雨云进行自动签到的Python脚本。
- 请注意 这只是一个demo，仅供学习参考，不保证能够长期使用。
## 功能说明

- 支持多账号登录和签到
- 程序将在每天的0-10随机签到一次
- 通过电子邮件发送签到结果的通知


## 使用说明

1. 安装依赖库：在运行代码之前，请确保已安装以下依赖库：
   - requests
   - email
   - apscheduler
   - python-dotenv
  
   ```bash
   pip install requests email apscheduler python-dotenv
   ```
   如果你使用python3，你可能需要使用pip3来安装依赖库。
   ```bash
   pip3 install requests email apscheduler python-dotenv
   ```
   - 如果您使用的是虚拟环境，请确保已经激活了虚拟环境再执行上述命令。
2. 设置环境变量：在运行代码之前，请确保已设置以下环境变量：
   ```
   cp .env.example .env 
   ```
   - USER_ID: 用户ID，用逗号分隔
   - USER_PASSWORD: 用户密码，用逗号分隔，顺序与用户ID对应
   - API_KEYS: API Key，用逗号分隔，顺序与用户ID对应
   - API_KEY_REMARKS: API Key的备注，用逗号分隔，顺序与API Key对应
   - NOTIFICATION_EMAILS: API Key的通知邮箱，用逗号分隔，顺序与API Key对应
   - TASK_NAME: 签到任务名称
   - SMTP_SERVER: SMTP服务器地址
   - SMTP_PORT: SMTP服务器端口号
   - SMTP_USERNAME: 邮箱用户名
   - SMTP_PASSWORD: 邮箱密码
   - SENDER_EMAIL: 发件人邮箱

3. 运行代码：使用以下命令运行代码：
   ```
   python app.py
   ```
   如果你使用python3，你可能需要使用python3来运行代码。
   ```
   python3 app.py
   ```

4. 定时任务：代码中已包含定时任务的设置，可以根据需要进行调整。


