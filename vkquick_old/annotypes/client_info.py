class ClientInfo:
    """
    Возвращает информацию о пользователе из ```event.object.client_info```
    """

    @classmethod
    def prepare(cls, argname, event, func, bin_stack):
        return event.object.client_info
