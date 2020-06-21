from json import dumps


class UI:
    """
    Add to vk ui incpasulations ability
    creating by dict (JSON scheme) and converting
    by __repr__
    """
    def __repr__(self) -> str:
        """
        Create for sending
        """
        return dumps(self.info, ensure_ascii=False)
        
    @classmethod
    def by(cls, pre_json: dict):
        """
        Init by dict
        """
        self = object.__new__(cls)
        self.info = pre_json
        return self
