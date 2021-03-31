class BadArgumentError(Exception):
    def __init__(self, *, remain_string: str, extra: dict):
        self.remain_string = remain_string
