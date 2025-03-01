import json
from .util import convert_data_keys


class Data:
    def __init__(self, data_dict: dict):
        self.type = data_dict.get('type', "")
        self.data = data_dict.get('data', [])
        self.dic_extra = data_dict.get('dic_extra', {})
        self.extra = data_dict.get('extra', None)

    def __repr__(self):
        return f"Data(type={self.type}, data={self.data}, dic_extra={self.dic_extra}, extra={self.extra})"


class Reply:
    def __init__(self, json_str: str):
        # 将输入的JSON字符串转换为Python字典
        data_dict = json.loads(json_str)

        # 提取各个字段
        self.err_code = data_dict.get('err_code', 0)
        self.err_message = data_dict.get('err_message', "")
        self.resp = Data(data_dict.get('data', {}))

    def __repr__(self):
        return f"Reply(err_code={self.err_code}, err_message={self.err_message}, data={self.resp})"

    def convert_data(self):
        if self.resp.data is None:
            self.resp.data = []

        self.resp.data = convert_data_keys(self.resp.data)
