try:
    # ^= 3.8
    import importlib.metadata as metadata
except ImportError:
    import importlib as metadata


__version__ = metadata.version(__name__)
