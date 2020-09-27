import enum


class BuiltinSignals(enum.Enum):
    STARTUP = enum.auto()
    SHUTDOWN = enum.auto()


class SignalHandler:
    ...
