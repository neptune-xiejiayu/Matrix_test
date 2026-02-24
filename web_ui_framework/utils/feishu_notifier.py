import os


class FeishuNotifier:
    def __init__(self, webhook=None):
        self.webhook = webhook or os.getenv('FEISHU_WEBHOOK')

    def send(self, title, text):
        # 占位：在实际使用时实现 HTTP POST 到飞书机器人
        if not self.webhook:
            return False
        # 示例返回 True 表示已“发送”
        return True
