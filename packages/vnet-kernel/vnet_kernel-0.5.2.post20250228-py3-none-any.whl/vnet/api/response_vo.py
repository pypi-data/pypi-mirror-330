import json


class ResponseVO:
    """响应对象，用于构造JSON格式响应"""

    def __init__(self, status: str, message: str = ""):
        self.status = status
        self.message = message

    @staticmethod
    def unknown_action() -> "ResponseVO":
        return ResponseVO("[ERROR]", "Unknown action")

    def to_json(self) -> str:
        """将响应对象转化为JSON字符串"""
        data = {"status": self.status}
        if self.message:
            data["message"] = self.message
        return json.dumps(data)
