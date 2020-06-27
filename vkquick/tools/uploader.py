from abc import ABC, abstractmethod


class Uploader:
    """
    Наследуйтесь, чтобы использовать в attachment у Message
    """
    @abstractmethod
    def __repr__(self):
        """
        Attachment-представление
        """
