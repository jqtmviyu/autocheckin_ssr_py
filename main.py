import logging,requests,json,sys
from config import account,wecom_bot,headers

# 会话保持
session = requests.session()
# 设置header
session.headers.update(headers)


# 日志模块
# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
# logger = logging.getLogger()

# 兼容pm2使用流模式
# 创建一个logger
logger = logging.getLogger("ssr")
# 设置日志级别（可选）
logger.setLevel(logging.INFO)
# 创建一个handler，将日志发送到stdout
stdout_handler = logging.StreamHandler(sys.stdout)
# 创建一个formatter，定义日志输出格式
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# 将formatter添加到handler
stdout_handler.setFormatter(formatter)
# 将handler添加到logger
logger.addHandler(stdout_handler)



# 登录
def login():
  logger.info('开始登录')
  try:
    url = account['url']+'/auth/login'
    data = {"email":account["email"],"passwd":account["password"]}
    msg = session.post(url, data=data)
    text = json.loads(msg.text)
    if msg.status_code == 200 and text["ret"] == 1:
      logger.info(text["msg"])
      return True
    else:
      logger.error(text["msg"])
      return False
  except Exception as e:
    logger.error(e)
    return False


# 签到
def checkin():
  logger.info('开始签到')
  try:
    url = account['url']+'/user/checkin'
    msg = session.post(url)
    text = json.loads(msg.text)
    if msg.status_code == 200 and text["ret"] == 1:
      logger.info(text["msg"])
    else:
      logger.error(text["msg"])
    return text["msg"]
  except Exception as e:
    logger.error(e)
    return "抛出异常"


# 企业微信群机器人通知
def notice(content):
  logger.info('发送通知')
  data = {
    "msgtype": "text",
    "text": {
      "content": f"ssr签到 \n\n {content}",
      "mentioned_mobile_list": [wecom_bot["telphone"]]
    }
  }
  data=json.dumps(data, ensure_ascii=False)
  try:
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={wecom_bot['key']}"
    msg = session.post(url, data=data)
    text = json.loads(msg.text)
    if msg.status_code == 200 and text["errcode"] == 0:
      logger.info(text["errmsg"])
      logger.info('发送成功')
    else:
      logger.error("发送失败")
  except Exception as e:
    logger.error(e)


# 入口
if __name__ == '__main__':
  login_res = login()
  if login_res :
    checkin_res = checkin()
    notice(checkin_res)
