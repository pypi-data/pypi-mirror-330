import requests
from datetime import datetime

class MyDataClient:
    def __init__(self, api_key=None, base_url="http://xyz.fuzefuze.top:8080"):
        """
        初始化客户端
        :param api_key: 用户的API密钥
        :param base_url: API 基础URL
        """
        self.api_key = api_key
        self.base_url = base_url

    def validate_date(self, date: str) -> bool:
        """
        验证日期格式是否为 YYYY-MM-DD
        """
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def get_stock_list(self, date: str):
        """
        调用API处理器
        :param date: 需要访问的日期, 必须是YYYY-MM-DD格式
        :return: 当日的选股和持仓数据
        """
        if not self.validate_date(date):
            raise ValueError("Date must be in YYYYMMDD format")

        url = f"{self.base_url}/api/process"
        headers = {"Content-Type": "application/json"}
        payload = {"input_data": date}

        if self.api_key:
            headers['Authorization'] = self.api_key

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()  # 如果请求失败，抛出异常
            return response.json()
        except requests.exceptions.HTTPError as err:
            print(f"HTTP Error: {err}")
            print(f"Response: {response.text}")  # 打印服务器返回的具体错误信息
            raise